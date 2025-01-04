<?php 

function get_jobs($responseData) {
    $cv = $responseData->cv ?? null;
    $cvk = $responseData->cv_keskus ?? null;
    $jobs = get_combined_jobs_sorted_by_time($cv, $cvk);

    return $jobs;
}

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
    $contains_comma = strpos($salary, ".");

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

function get_combined_jobs_sorted_by_time($cv, $cvk) {
    if (empty($cv) && empty($cvk)) return array();
    if (empty($cv)) return $cvk;
    if (empty($cvk)) return $cv;
    
    $jobs = array();
    $cvLength = count($cv);
    $cvkLength = count($cvk);
    $i = $j = 0;

    while ($i < $cvLength && $j < $cvkLength) {
        if (new DateTime($cv[$i]->publishDate) >= new DateTime($cvk[$j]->time)) {
            array_push($jobs, $cv[$i]);
            $i++;
        } else {
            array_push($jobs, $cvk[$j]);
            $j++;
        }
    }
    
    for (; $i < $cvLength; $i++) array_push($jobs, $cv[$i]);
    for (; $j < $cvkLength; $j++) array_push($jobs, $cvk[$j]);

    return $jobs;
}
