<?php
    $API_URL = "http://localhost:5000/api/jobs";
    $start = $_GET['start'];

    $json_data = file_get_contents($API_URL);
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
                <?php foreach($cv as $index => $value): ?>
                <li class="job">
                    <h3 class="job__position">
                        <a href="<?= "https://cv.ee/et/vacancy/{$value->id}" ?>"><?= $value->positionTitle ?></a>
                    </h3>
                    <div class="job__info">
                        <span class="job__info__company"><?= $value->employerName ?></span>
                        <div class="job__info__details">
                            <span class="job__row__detail"><?= salary_text($value->salaryFrom, $value->salaryTo) ?></span>
                            <span class="job__row__detail"><?= $value->publishDate ?></span>
                        </div>
                    </div>
                </li>
                <?php endforeach; ?>

                <?php foreach($cv_keskus as $index => $value): ?>
                <li class="job">
                    <h3 class="job__position">
                        <a href="<?= $value->link ?>"><?= $value->position ?></a>
                    </h3>
                    <div class="job__info">
                        <span class="job__info__company"><?= $value->company ?></span>
                        <div class="job__info__details">
                            <span class="job__row__detail"><?= salary_text($value->salary, null) ?></span>
                            <span class="job__row__detail"><?= $value->time ?></span>
                        </div>
                    </div>
                </li>
                <?php endforeach; ?>
            </ul>
        </section>
    </main>
  </body>
</html>