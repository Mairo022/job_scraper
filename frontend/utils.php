<?php 
function format_salary_cvkeskus($salary) {
    if (!is_null($salary)) return "{$salary} | ";
}

function format_salary_cv($salary_from, $salary_to) {
    if (is_null($salary_from) && !is_null($salary_to)) {
        $rate = get_salary_rate($salary_to);

        return "Kuni {$salary_to} " . $rate . " | ";
    }
    if (!is_null($salary_from) && is_null($salary_to)) {
        $rate = get_salary_rate($salary_from);

        return "{$salary_from} " . $rate . " | ";
    }
    if (!is_null($salary_from) && !is_null($salary_to)) {
        $rate = get_salary_rate($salary_from);

        return "{$salary_from} - {$salary_to} " . $rate . " | ";
    }

    return "";
}

function get_salary_rate($salary) {
    $salary_len = strlen($salary);
    $contains_comma = str_contains($salary, ".");

    if (($contains_comma && $salary_len < 4) || (!$contains_comma && $salary_len < 3)) {
        return "€/tunnis";
    }

    return "€/kuus";
}

function format_time($time_arg_str) {
    $time_arg = new DateTime($time_arg_str);
    $time_now = new DateTime();
    $time_diff = $time_now->diff($time_arg);

    $days = $time_diff->d;
    $hours = $time_diff->h;
    $minutes = $time_diff->i;
    $seconds = $time_diff->s;

    if ($days > 0) {
        if ($days == 1) return "Päev tagasi";
        if ($days < 7) return "{$days} p. tagasi";
        if ($days < 14) return "Nädal tagasi";
    
        return round($days/7) . " näd. tagasi";
    }
    
    if ($hours > 0) return $hours == 1 ? "Tund tagasi" : "{$hours} tundi tagasi";
    if ($minutes > 0) return $minutes == 0 ? "Minut tagasi" : "{$minutes} min. tagasi";
    if ($seconds > 0) return "{$seconds} s. tagasi";
}

function get_location_id() {
    return isset($_GET['location']) ? intval($_GET['location']) : 2;
}

function get_offsets() {
    $offset = intval($_GET['start'] ?? 0);
    $offsetNext = $offset + JOBS_PER_SITE;
    $offsetPrevious = $offset >= JOBS_PER_SITE ? $offset - JOBS_PER_SITE : 0;

    return [$offset, $offsetPrevious, $offsetNext];
}

function get_combined_jobs_sorted_by_time($cv, $cvk) {
    if (empty($cv) && empty($cv_keskus)) return array();
    if (empty($cv)) return $cvk;
    if (empty($cvk)) return $cv;
    
    $jobs = array();
    $tempJobsCV = array();
    $tempJobsCVK = array();

    for ($i = 0; $i < JOBS_PER_SITE; $i++) {
        $timeCV = new DateTime($cv[$i]->publishDate);
        $timeCVK = new DateTime($cvk[$i]->time);
        $isCVNewer = $timeCV > $timeCVK;

        if ($isCVNewer) {
            foreach($tempJobsCV as $job) array_push($jobs, $job);
            foreach($tempJobsCVK as $index => $job) {
                if ($timeCV < new DateTime($job->time)) {
                    array_push($jobs, $job);
                    unset($tempJobsCVK[$index]);
                } else break;
            }

            array_push($jobs, $cv[$i]);
            array_push($tempJobsCVK, $cvk[$i]);
            $tempJobsCV = array();
        }

        if (!$isCVNewer) {
            foreach($tempJobsCVK as $job) array_push($jobs, $job);
            foreach($tempJobsCV as $index => $job) {
                if ($timeCVK < new DateTime($job->publishDate)) {
                    array_push($jobs, $job);
                    unset($tempJobsCV[$index]);
                } else break;
            }

            array_push($jobs, $cvk[$i]);
            array_push($tempJobsCV, $cv[$i]);
            $tempJobsCVK = array();
        }
    }

    // Add remaining jobs from tempJobs arrays
    $lengthTempJobsCV = count($tempJobsCV);
    $lengthTempJobsCVK = count($tempJobsCVK);

    if ($lengthTempJobsCV > 0) {
        foreach($tempJobsCV as $index => $job) {
            if (isset($tempJobsCVK[$index])) {
                $isCVNewer = new DateTime($job->publishDate) > new DateTime($tempJobsCVK[$index]->time);

                if ($isCVNewer) {
                    array_push($jobs, $job);
                } else {
                    array_push($jobs, $tempJobsCVK[$index]);
                }
            } else {
                array_push($jobs, $job);
                continue;
            }

            if ($index == $lengthTempJobsCV - 1) {
                for ($j = $index; $j < $lengthTempJobsCVK; $j++)
                    array_push($jobs, $tempJobsCVK[$j]);
            }
        }
    } else foreach($tempJobsCVK as $job) array_push($jobs, $job);

    return $jobs;
}