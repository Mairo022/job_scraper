<?php
    $TOTAL_JOBS = 30;
    $API_URL = "http://localhost:5000/api";

    $start = $_GET['start'] ?? 0;
    $url_jobs ="{$API_URL}/jobs?start={$start}";

    $json_data = file_get_contents($url_jobs);
    $response_data = json_decode($json_data);

    $cv = $response_data->cv;
    $cv_keskus = $response_data->cv_keskus;

    function salary_text_cv_keskus($salary) {
        if (!is_null($salary)) {
            return "{$salary} | ";
        }
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
            <?php for ($i = 0; $i < $TOTAL_JOBS; $i++): ?>
                <?php if (isset($cv[$i])): ?>
                    <li class="job job--cv">
                        <h3 class="job__position">
                            <a href="<?= "https://cv.ee/et/vacancy/{$cv[$i]->id}" ?>"><?= $cv[$i]->positionTitle ?></a>
                        </h3>
                        <div class="job__info">
                            <span class="job__info__company"><?= $cv[$i]->employerName ?></span>
                            <div class="job__info__details">
                                <span class="job__row__detail"><?= salary_text_cv($cv[$i]->salaryFrom, $cv[$i]->salaryTo) ?></span>
                                <span class="job__row__detail"><?= format_time($cv[$i]->publishDate) ?></span>
                            </div>
                        </div>
                    </li>
                <?php endif; ?>

                <?php if (isset($cv_keskus[$i])): ?>
                    <li class="job job--cvkeskus">
                        <h3 class="job__position">
                            <a href="<?= $cv_keskus[$i]->link ?>"><?= $cv_keskus[$i]->position ?></a>
                        </h3>
                        <div class="job__info">
                            <span class="job__info__company"><?= $cv_keskus[$i]->company ?></span>
                            <div class="job__info__details">
                                <span class="job__row__detail"><?= salary_text_cv_keskus($cv_keskus[$i]->salary, null) ?></span>
                                <span class="job__row__detail"><?= ucfirst($cv_keskus[$i]->time) ?></span>
                            </div>
                        </div>
                    </li>
                <?php endif; ?>
            <?php endfor; ?>
            </ul>
            <div class="jobs__paging">
                <a 
                class="jobs__paging__page<?= intval($start) == 0 ? ' disabled' : '' ?>" 
                href="?start=<?= intval($start) <= 30 ? "0" : intval($start)-30 ?>"
                >
                <svg class="jobs__paging__page__svg" strokeWidth={0.8} stroke="currentColor" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" xmlSpace="preserve">
                    <path d="M17.2 23.7 5.4 12 17.2.3l1.3 1.4L8.4 12l10.1 10.3z" />
                </svg>
            </a>
                <a 
                class="jobs__paging__page" 
                href="?start=<?= intval($start)+30 ?>"
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
