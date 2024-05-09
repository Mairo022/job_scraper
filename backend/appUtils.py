import os
import logging
import time

from constants import LOCATIONS_AVAILABLE, CACHE_LIFESPAN
from pages import Pages


def is_cache_fresh(cache_time):
    return time.time() - cache_time < CACHE_LIFESPAN


def initialise_pages():
    pages = dict()

    for location in LOCATIONS_AVAILABLE:
        pages[location] = Pages(location)

    return pages


def evaluate_ads_age(cv, cvk):
    cv_first_ad_date = cv[0].get('publishDate')
    cvk_first_ad_date = cvk[0].get('time')
    cv_last_ad_date = cv[-1].get('publishDate')
    cvk_last_ad_date = cvk[-1].get('time')

    cvk_ads_older = cv_last_ad_date > cvk_first_ad_date
    cv_ads_older = cvk_last_ad_date > cv_first_ad_date

    return [cv_ads_older, cvk_ads_older]


def get_return_data(cv_ads_older, cvk_ads_older, cv, cv_keskus):
    if cv_ads_older:
        return {"cv_keskus": cv_keskus, "cv": []}

    if cvk_ads_older:
        return {"cv_keskus": [], "cv": cv}

    return {"cv_keskus": cv_keskus, "cv": cv}


def initialise_logging():
    log_folder = os.path.join(os.getcwd(), 'logs')

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file = os.path.join(log_folder, "app.log")
    logging.basicConfig(filename=log_file, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')