import os
import logging
import time

import scraper
from constants import LOCATIONS_AVAILABLE, CACHE_LIFESPAN
from pages import Pages


def initialise_pages():
    pages = dict()

    for location in LOCATIONS_AVAILABLE:
        pages[location] = Pages(location)

    return pages


def get_jobs(offset, location, cache, real_pages, category):
    if offset == 0 and category == 0:
        cached_data_item = cache.get(str(location))

        if cached_data_item and is_cache_fresh(cached_data_item.get("time")):
            return cached_data_item.get("data")

    start_cv, start_cvk = real_pages.get_pages(offset)
    cvk = scraper.get_jobs_cv_keskus(start_cvk, location, category)
    cv = scraper.get_jobs_cv(start_cv, location, category)
    cv_ads_older, cvk_ads_older = evaluate_ads_age(cv, cvk)

    if category != 0:
        return assign_jobs(cv_ads_older, cvk_ads_older, cv, cvk)

    real_pages.set_pages(offset, start_cv, start_cvk, cv_ads_older, cvk_ads_older)

    if offset == 0 and cv and cvk:
        cache[str(location)] = {
            "data": {"cv_keskus": cvk, "cv": cv},
            "time": time.time()
        }

    job_ads = assign_jobs(cv_ads_older, cvk_ads_older, cv, cvk)

    return job_ads


def initialise_logging():
    log_folder = os.path.join(os.getcwd(), 'logs')

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file = os.path.join(log_folder, "app.log")
    logging.basicConfig(filename=log_file, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def assign_jobs(cv_ads_older, cvk_ads_older, cv, cv_keskus):
    if cv_ads_older:
        return {"cv_keskus": cv_keskus, "cv": []}

    if cvk_ads_older:
        return {"cv_keskus": [], "cv": cv}

    return {"cv_keskus": cv_keskus, "cv": cv}


# Checks whether one's last ad is newer than other's first ad
def evaluate_ads_age(cv, cvk):
    if not cv or not cvk:
        return [False, False]

    cv_first_ad_date = cv[0].get('publishDate')
    cvk_first_ad_date = cvk[0].get('time')
    cv_last_ad_date = cv[-1].get('publishDate')
    cvk_last_ad_date = cvk[-1].get('time')

    cvk_ads_older = cv_last_ad_date > cvk_first_ad_date
    cv_ads_older = cvk_last_ad_date > cv_first_ad_date

    return [cv_ads_older, cvk_ads_older]


def is_cache_fresh(cache_time):
    return time.time() - cache_time < CACHE_LIFESPAN
