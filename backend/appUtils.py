import os
import logging
import time

from constants import LOCATIONS_AVAILABLE, CACHE_LIFESPAN


def is_cache_fresh(cache_time):
    return time.time() - cache_time < CACHE_LIFESPAN


def initialise_pages():
    pages = dict()

    for location in LOCATIONS_AVAILABLE:
        pages[location] = {
            "pages": {
                0: {'cv': 0, 'cvk': 0}
            },
            "last_updated": time.time()
        }

    return pages


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