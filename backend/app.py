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
    start = int(request.args.get("start", 0))
    location = int(request.args.get("location", 0))

    if start < 0 or start % ADS_LIMIT != 0:
        abort(400, "Invalid offset")

    if location not in LOCATIONS_AVAILABLE:
        abort(400, "Invalid location id")

    if start == 0:
        cached_data_item = app.cached_data.get(str(location))

        if cached_data_item and is_cache_fresh(cached_data_item.get("time")):
            return jsonify(cached_data_item.get("data"))

    real_pages = app.real_pages[location]
    start_cv, start_cvk = real_pages.get_pages(start)

    cv_keskus = scraper.get_jobs_cv_keskus(start_cvk, location)
    cv = scraper.get_jobs_cv(start_cv, location)

    cv_ads_older, cvk_ads_older = evaluate_ads_age(cv, cv_keskus)

    combined = {"cv_keskus": cv_keskus, "cv": cv}

    real_pages.set_pages(start, start_cv, start_cvk, cv_ads_older, cvk_ads_older)

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
