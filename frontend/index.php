<?php
    $AMOUNT_OF_JOBS_PER_SITE = 30;
    $API_URL = "http://localhost:5000/api";

    $offset = intval($_GET['start']);
    $offsetNext = $offset + 30;
    $offsetPrevious = $offset >= 30 ? $offset - 30 : 0;

    $url_jobs ="{$API_URL}/jobs?start={$offset}";

    $json_data = file_get_contents($url_jobs);
    $response_data = json_decode($json_data);

    $cv = $response_data->cv;
    $cv_keskus = $response_data->cv_keskus;

    if (!empty($cv) || !empty($cv_keskus)) {
        $jobs = get_combined_jobs_sorted_by_time($cv, $cv_keskus);
    }

    function get_combined_jobs_sorted_by_time($cv, $cvk) {
        global $AMOUNT_OF_JOBS_PER_SITE;
        $jobs = array();
        $tempJobsCV = array();
        $tempJobsCVK = array();

        for ($i = 0; $i < $AMOUNT_OF_JOBS_PER_SITE; $i++) {
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

    function salary_text_cv_keskus($salary) {
        if (!is_null($salary)) return "{$salary} | ";
    }

    function salary_text_cv($salary_from, $salary_to) {
        if (is_null($salary_from) && !is_null($salary_to)) {
            $rate = salary_rate($salary_to);

            return "Kuni {$salary_to} " . $rate . " | ";
        }
        if (!is_null($salary_from) && is_null($salary_to)) {
            $rate = salary_rate($salary_from);

            return "{$salary_from} " . $rate . " | ";
        }
        if (!is_null($salary_from) && !is_null($salary_to)) {
            $rate = salary_rate($salary_from);

            return "{$salary_from} - {$salary_to} " . $rate . " | ";
        }

        return "";
    }

    function salary_rate($salary) {
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
        
        if ($hours > 0) {
            return $hours == 1 ? "Tund tagasi" : "{$hours} tundi tagasi";
        }
        
        if ($minutes > 0) {
            return $minutes == 0 ? "Minut tagasi" : "${minutes} min. tagasi";
        }
        
        if ($seconds > 0) {
            return "{$seconds} s. tagasi";
        }
    }
?>
<!DOCTYPE html>
<html lang="ee">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="./style.css">
    <link rel="icon" href="./favicon.ico" type="image/x-icon">
    <script defer src="script.js"></script>
    <title>Jobs</title>
  </head>
  <body>
    <main>
        <header class="header">
            <h1 class="header__title">Jobs</h1>
            <p class="header__location">Tartu</p>
        </header>
        <section class="jobs">
            <div class="nav">
                <button class="nav__button active" id="allBtn" onclick="navBtnClick('all')">All</button>
                <button class="nav__button" id="cvBtn" onclick="navBtnClick('cv')">CV</button>
                <button class="nav__button" id="cvkeskusBtn" onclick="navBtnClick('cvkeskus')">CV Keskus</button>
            </div>
            <ul>
            <?php foreach ($jobs as $job): ?>
                <?php if (isset($job->positionTitle)): ?>
                    <li class="job job--cv">
                        <h3 class="job__position">
                            <a href="<?= "https://cv.ee/et/vacancy/{$job->id}" ?>"><?= $job->positionTitle ?></a>
                        </h3>
                        <div class="job__info">
                            <span class="job__info__company"><?= $job->employerName ?></span>
                            <div class="job__info__details">
                                <span class="job__row__detail"><?= salary_text_cv($job->salaryFrom, $job->salaryTo) ?></span>
                                <span class="job__row__detail"><?= format_time($job->publishDate) ?></span>
                            </div>
                        </div>
                    </li>
                <?php endif; ?>
                <?php if (isset($job->position)): ?>
                    <li class="job job--cvkeskus">
                        <h3 class="job__position">
                            <a href="<?= $job->link ?>"><?= $job->position ?></a>
                        </h3>
                        <div class="job__info">
                            <span class="job__info__company"><?= $job->company ?></span>
                            <div class="job__info__details">
                                <span class="job__row__detail"><?= salary_text_cv_keskus($job->salary, null) ?></span>
                                <span class="job__row__detail"><?= format_time($job->time) ?></span>
                            </div>
                        </div>
                    </li>
                <?php endif; ?>
            <?php endforeach; ?>
            </ul>
            <div class="jobs__paging">
                <a 
                class="jobs__paging__page<?= $offset == 0 ? ' disabled' : '' ?>" 
                href="?start=<?= $offsetPrevious ?>"
                >
                <svg class="jobs__paging__page__svg" strokeWidth={0.8} stroke="currentColor" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" xmlSpace="preserve">
                    <path d="M17.2 23.7 5.4 12 17.2.3l1.3 1.4L8.4 12l10.1 10.3z" />
                </svg>
            </a>
                <a 
                class="jobs__paging__page" 
                href="?start=<?= $offsetNext ?>"
                >
                <svg class="jobs__paging__page__svg"strokeWidth={0.8} stroke="currentColor" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" xmlSpace="preserve">
                    <path d="M6.8 0.3 18.6 12 6.8 23.7 5.5 22.3 15.6 12 5.5 1.7z" />
                </svg>
            </a>
            </div>
        </section>
    </main>
  </body>
</html>
