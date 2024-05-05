from flask import Flask, jsonify, request, abort

from appUtils import *
from constants import LOCATIONS_AVAILABLE, ADS_LIMIT

import scraper
import time

app = Flask(__name__)

app.cached_data = dict()
app.real_pages = initialise_pages()


@app.route("/api/jobs", methods=['GET'])
def jobs_data():
    start = start_cv = start_cvk = int(request.args.get("start", 0))
    location = int(request.args.get("location", 0))

    if start < 0:
        abort(400, "Invalid offset")

    if location not in LOCATIONS_AVAILABLE:
        abort(400, "Invalid location id")

    if start == 0:
        cached_data_item = app.cached_data.get(str(location))

        if cached_data_item and is_cache_fresh(cached_data_item.get("time")):
            return jsonify(cached_data_item.get("data"))

    location_real_pages = app.real_pages.get(location)
    location_updated = location_real_pages.get("last_updated")
    location_pages = location_real_pages.get("pages")

    current_pages = location_pages.get(start)
    previous_pages = location_pages.get(start-ADS_LIMIT)

    if is_cache_fresh(location_updated):
        if current_pages:
            start_cv = current_pages.get("cv")
            start_cvk = current_pages.get("cvk")

        if previous_pages and not current_pages:
            previous_page_cv = previous_pages.get("cv")
            previous_page_cvk = previous_pages.get("cvk")

            if previous_page_cv + ADS_LIMIT != start:
                start_cv = previous_page_cv

            if previous_page_cvk + ADS_LIMIT != start:
                start_cvk = previous_page_cvk

    cv_keskus = scraper.get_jobs_cv_keskus(start_cvk, location)
    cv = scraper.get_jobs_cv(start_cv, location)

    cv_first_ad_date = cv[0].get('publishDate')
    cvk_first_ad_date = cv_keskus[0].get('time')
    cv_last_ad_date = cv[-1].get('publishDate')
    cvk_last_ad_date = cv_keskus[-1].get('time')

    cvk_ads_older = cv_last_ad_date > cvk_first_ad_date
    cv_ads_older = cvk_last_ad_date > cv_first_ad_date

    try:
        next_start = start + ADS_LIMIT

        if current_pages:
            cur_cv = current_pages.get("cv")
            cur_cvk = current_pages.get("cvk")

            if cvk_ads_older:
                location_pages[next_start] = {"cv": cur_cv + ADS_LIMIT, "cvk": cur_cvk}

            if cv_ads_older:
                location_pages[next_start] = {"cv": cur_cv, "cvk": cur_cvk + ADS_LIMIT}

        else:
            location_pages[start] = {"cv": start, "cvk": start}

            if cvk_ads_older:
                location_pages[next_start] = {"cv": next_start, "cvk": start}
            elif cv_ads_older:
                location_pages[next_start] = {"cv": start, "cvk": next_start}
            else:
                location_pages[next_start] = {"cv": next_start, "cvk": next_start}

        location_real_pages["last_updated"] = time.time()

    except KeyError as e:
        print("KeyError", e)

    except Exception as e:
        print(repr(e))

    combined = {"cv_keskus": cv_keskus, "cv": cv}

    if start == 0 and cv and cv_keskus:
        app.cached_data[str(location)] = {
            "data": combined,
            "time": time.time()
        }

    return_data = get_return_data(cv_ads_older, cvk_ads_older, cv, cv_keskus)

    return jsonify(return_data)


with app.app_context():
    initialise_logging()


if __name__ == '__main__':
    app.run()
