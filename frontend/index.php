<?php
    require 'constants.php';
    require 'utils.php';

    $locationID = get_location_id();
    $categoryID = get_category_id();
    [$offset, $offsetPrevious, $offsetNext] = get_offsets();

    $urlJobs = API_URL . "/jobs?location={$locationID}&start={$offset}&category={$categoryID}";

    $response = @file_get_contents($urlJobs);
    $responseData = json_decode($response);

    $cv = $responseData->cv ?? null;
    $cvk = $responseData->cv_keskus ?? null;

    $jobs = get_combined_jobs_sorted_by_time($cv, $cvk);
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
        </header>
        <section class="jobs">
            <a class="it_filter" href='<?= $categoryID == 0 ? "?location=0&category=1" : "?location={$locationID}&category=0 " ?>'>
                <div class="it_filter__status"></div>
                <span class="it_filter__text">IT only</span>
            </a>
            <div class="location-menu">
                <div class="location__select">
                    <div class="location__select-active"><?= LOCATION_DEFAULT ?></div>
                    <div class="location__select-button">
                        <svg fill="#444" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 330 330" xml:space="preserve"><path id="XMLID_222_" d="M250.606,154.389l-150-149.996c-5.857-5.858-15.355-5.858-21.213,0.001 c-5.857,5.858-5.857,15.355,0.001,21.213l139.393,139.39L79.393,304.394c-5.857,5.858-5.857,15.355,0.001,21.213 C82.322,328.536,86.161,330,90,330s7.678-1.464,10.607-4.394l149.999-150.004c2.814-2.813,4.394-6.628,4.394-10.606 C255,161.018,253.42,157.202,250.606,154.389z"></path></svg>                    
                    </div>
                </div>
                <ul class="location__options">
                    <?php foreach (LOCATIONS as $id => $location): ?>
                        <li class="location__options__option" data-id="<?= $id ?>">
                            <a class="location__options__option__link" href='<?= "?location=$id&start=0&category=$categoryID" ?>'>
                                <?= $location ?>
                            </a>
                        </li>
                    <?php endforeach; ?>
                </ul>
            </div>
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
                                <span class="job__row__detail"><?= format_salary_cv($job->salaryFrom, $job->salaryTo) ?></span>
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
                                <span class="job__row__detail"><?= format_salary_cvkeskus($job->salary) ?></span>
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
                href='<?= "?location={$locationID}&start={$offsetPrevious}&category={$categoryID}" ?>'
                >
                <svg class="jobs__paging__page__svg" strokeWidth={0.8} stroke="currentColor" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" xmlSpace="preserve">
                    <path d="M17.2 23.7 5.4 12 17.2.3l1.3 1.4L8.4 12l10.1 10.3z" />
                </svg>
            </a>
                <a 
                class="jobs__paging__page" 
                href='<?= "?location={$locationID}&start={$offsetNext}&category={$categoryID}" ?>'
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
