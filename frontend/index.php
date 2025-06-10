<?php
    require 'constants.php';
    require 'renderUtils.php';
    require 'requestUtils.php';

    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);

    $ip = get_ip_address();
    $locationID = get_location_id();
    $categoryID = get_category_id();
    [$offset, $offsetPrevious, $offsetNext] = get_offsets();

    $url = API_URL . "/jobs?location={$locationID}&start={$offset}&category={$categoryID}";
    $jobsRequest = request_job_data($url, $ip);
    $responseCode = $jobsRequest["response_code"];
    $responseData = $jobsRequest["response_data"];

    $jobs = get_jobs($responseData);
?>
<!DOCTYPE html>
<html lang="ee">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="./style.css?v108">
    <link rel="icon" href="./favicon.ico" type="image/x-icon">
    <script defer src="script.js?v107"></script>
    <title>Jobs</title>
  </head>
  <body>
    <main>
        <header class="header">
            <h1 class="header__title">Jobs</h1>
        </header>
        <section class="jobs">
            <div class="filters">
                <div class="location_filter">
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
                <a class="filter" href='<?= $categoryID == 0 ? "?location=0&category=1" : "?location={$locationID}&category=0 " ?>'>
                    <div class="filter__status" id="it_filter_status"></div>
                    <span class="filter__text">IT Töö</span>
                </a>
                <button class="filter" id="saved_view_btn">
                    <span class="filter__status" id="saved_view_status"></span>
                    <span class="filter__text filter__text">Salvestatud</span>
                </button>
            </div>
            <ul>
            <?php if ($responseCode !== 200): ?>
                <div class="error">
                    <?= $responseData ?>
                </div>
            <?php endif; ?>
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
                        <button type="button" class="job__save" aria-label="Salvesta"><svg fill="#000000" height="34px" width="34px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve"><g><g><g><path d="M426.027,209.813c-1.493-4.267-5.547-7.147-10.027-7.147H311.36l-40.213-95.787c-2.24-5.44-8.533-8-13.973-5.653 c-2.56,1.067-4.587,3.093-5.653,5.653l-40.213,95.787h-104.64c-5.867,0-10.667,4.8-10.667,10.667c0,3.2,1.493,6.187,3.947,8.213 L184,289.92l-35.84,112.427c-1.813,5.653,1.28,11.627,6.933,13.44c3.307,1.067,6.827,0.427,9.6-1.6l96.64-71.787l96.747,72.533 c4.693,3.52,11.413,2.56,14.933-2.133c2.027-2.773,2.667-6.293,1.6-9.6l-35.947-113.28l84.053-68.267 C426.24,218.773,427.52,213.973,426.027,209.813z M319.573,277.867c-3.413,2.773-4.8,7.36-3.413,11.52l28.053,88.533 l-76.48-57.28c-3.84-2.88-8.96-2.88-12.8,0l-76.587,56.747L206.4,289.6c1.387-4.16,0-8.747-3.413-11.52L136.64,224h81.707 c4.267,0,8.213-2.56,9.813-6.507l33.173-78.827l33.067,78.827c1.707,3.947,5.547,6.507,9.813,7.573h81.707L319.573,277.867z"/><path d="M256,0C114.88,0,0,114.88,0,256s114.88,256,256,256s256-114.88,256-256S397.12,0,256,0z M256,490.667 c-129.387,0-234.667-105.28-234.667-234.667S126.613,21.333,256,21.333S490.667,126.613,490.667,256S385.387,490.667,256,490.667 z"/></g></g></g></svg></button>
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
                        <button type="button" class="job__save" aria-label="Salvesta"><svg fill="#000000" height="34px" width="34px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve"><g><g><g><path d="M426.027,209.813c-1.493-4.267-5.547-7.147-10.027-7.147H311.36l-40.213-95.787c-2.24-5.44-8.533-8-13.973-5.653 c-2.56,1.067-4.587,3.093-5.653,5.653l-40.213,95.787h-104.64c-5.867,0-10.667,4.8-10.667,10.667c0,3.2,1.493,6.187,3.947,8.213 L184,289.92l-35.84,112.427c-1.813,5.653,1.28,11.627,6.933,13.44c3.307,1.067,6.827,0.427,9.6-1.6l96.64-71.787l96.747,72.533 c4.693,3.52,11.413,2.56,14.933-2.133c2.027-2.773,2.667-6.293,1.6-9.6l-35.947-113.28l84.053-68.267 C426.24,218.773,427.52,213.973,426.027,209.813z M319.573,277.867c-3.413,2.773-4.8,7.36-3.413,11.52l28.053,88.533 l-76.48-57.28c-3.84-2.88-8.96-2.88-12.8,0l-76.587,56.747L206.4,289.6c1.387-4.16,0-8.747-3.413-11.52L136.64,224h81.707 c4.267,0,8.213-2.56,9.813-6.507l33.173-78.827l33.067,78.827c1.707,3.947,5.547,6.507,9.813,7.573h81.707L319.573,277.867z"/><path d="M256,0C114.88,0,0,114.88,0,256s114.88,256,256,256s256-114.88,256-256S397.12,0,256,0z M256,490.667 c-129.387,0-234.667-105.28-234.667-234.667S126.613,21.333,256,21.333S490.667,126.613,490.667,256S385.387,490.667,256,490.667 z"/></g></g></g></svg></button>
                    </li>
                <?php endif; ?>
            <?php endforeach; ?>
            </ul>
            <?php if ($jobs): ?>
                <div class="jobs__paging">
                    <a 
                    class="jobs__paging__page<?= $offset == 0 ? ' disabled' : '' ?>" 
                    href='<?= "?location={$locationID}&start={$offsetPrevious}&category={$categoryID}" ?>'
                    >
                    <svg class="jobs__paging__page__svg" stroke="currentColor" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M17.2 23.7 5.4 12 17.2.3l1.3 1.4L8.4 12l10.1 10.3z" />
                    </svg>
                </a>
                    <a 
                    class="jobs__paging__page" 
                    href='<?= "?location={$locationID}&start={$offsetNext}&category={$categoryID}" ?>'
                    >
                    <svg class="jobs__paging__page__svg" stroke="currentColor" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M6.8 0.3 18.6 12 6.8 23.7 5.5 22.3 15.6 12 5.5 1.7z" />
                    </svg>
                </a>
                </div>
            <?php endif; ?>
        </section>
        <div class="glow_bg"></div>
        <div class="stars_bg"></div>
    </main>
  </body>
</html>
