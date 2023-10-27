<?php
    $TOTAL_JOBS = 30;
    $API_URL = "http://localhost:5000/api";

    $start = $_GET['start'];
    $url = $start ? "{$API_URL}/jobs?start={$start}" : "{$API_URL}/jobs";

    $json_data = file_get_contents($url);
    $response_data = json_decode($json_data);

    $cv = $response_data->cv;
    $cv_keskus = $response_data->cv_keskus;

    function salary_text($salary_from, $salary_to) {
        if (is_null($salary_from) && !is_null($salary_to)) {
            return "Kuni {$salary_to} | ";
        }
        if (!is_null($salary_from) && is_null($salary_to)) {
            return "{$salary_from} | ";
        }
        if (!is_null($salary_from) && !is_null($salary_to)) {
            return "{$salary_from} - {$salary_to} | ";
        }
        return "";
    }
?>
<!DOCTYPE html>
<html lang="ee">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="./style.css">
    <link rel="icon" href="./favicon.ico" type="image/x-icon">
    <title>Jobs</title>
  </head>
  <body>
    <main>
        <h1 class="title">Jobs</h1>
        <section class="jobs">
            <ul>
            <?php for ($i = 0; $i < $TOTAL_JOBS; $i++): ?>
                <?php if (isset($cv[$i])): ?>
                    <li class="job">
                        <h3 class="job__position">
                            <a href="<?= "https://cv.ee/et/vacancy/{$cv[$i]->id}" ?>"><?= $cv[$i]->positionTitle ?></a>
                        </h3>
                        <div class="job__info">
                            <span class="job__info__company"><?= $cv[$i]->employerName ?></span>
                            <div class="job__info__details">
                                <span class="job__row__detail"><?= salary_text($cv[$i]->salaryFrom, $cv[$i]->salaryTo) ?></span>
                                <span class="job__row__detail"><?= $cv[$i]->publishDate ?></span>
                            </div>
                        </div>
                    </li>
                <?php endif; ?>

                <?php if (isset($cv_keskus[$i])): ?>
                    <li class="job">
                        <h3 class="job__position">
                            <a href="<?= $cv_keskus[$i]->link ?>"><?= $cv_keskus[$i]->position ?></a>
                        </h3>
                        <div class="job__info">
                            <span class="job__info__company"><?= $cv_keskus[$i]->company ?></span>
                            <div class="job__info__details">
                                <span class="job__row__detail"><?= salary_text($cv_keskus[$i]->salary, null) ?></span>
                                <span class="job__row__detail"><?= $cv_keskus[$i]->time ?></span>
                            </div>
                        </div>
                    </li>
                <?php endif; ?>
            <?php endfor; ?>
            </ul>
            <div class="job__paging">
                <a 
                class="job__paging__page<?= intval($start) == 0 ? ' disabled' : '' ?>" 
                href="?start=<?= intval($start) <= 30 ? "0" : intval($start)-30 ?>"
                >
                Previous
            </a>
                <a 
                class="job__paging__page" 
                href="?start=<?= intval($start)+30 ?>"
                >
                Next
            </a>
            </div>
        </section>
    </main>
  </body>
</html>