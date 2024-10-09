<?php

function request_job_data($url, $ip) {
    $jobsRequest = curl_init($url);
    curl_setopt($jobsRequest, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($jobsRequest, CURLOPT_HTTPHEADER, ["X-Real-IP: {$ip}"]);

    $responseBody = curl_exec($jobsRequest);
    $responseCode = curl_getinfo($jobsRequest, CURLINFO_HTTP_CODE);
    $responseData = $responseCode === 200 ? json_decode($responseBody) : $responseBody;

    curl_close($jobsRequest);

    return [
        'response_code' => $responseCode,
        'response_data' => $responseData
    ];
}

function get_location_id() {
    return isset($_GET['location']) ? intval($_GET['location']) : 2;
}

function get_category_id() {
    return isset($_GET['category']) ? intval($_GET['category']) : 0;
}

function get_offsets() {
    $offset = intval($_GET['start'] ?? 0);
    $offsetNext = $offset + JOBS_PER_SITE;
    $offsetPrevious = $offset >= JOBS_PER_SITE ? $offset - JOBS_PER_SITE : 0;

    return [$offset, $offsetPrevious, $offsetNext];
}

function get_ip_address() {
    if (!empty($_SERVER["HTTP_X_REAL_IP"])) {
        return trim($_SERVER["HTTP_X_REAL_IP"]);
    } else {
        return $_SERVER["REMOTE_ADDR"];
    }
}
