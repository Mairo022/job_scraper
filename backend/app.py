from flask import Flask, jsonify, request, abort
from constants import LOCATIONS_AVAILABLE

import scraper
import time
import os
import logging

app = Flask(__name__)

app.cache_lifespan = 1800
app.cached_data = dict()


@app.route("/api/jobs", methods=['GET'])
def jobs_data():
    start = int(request.args.get("start", 0))
    location = int(request.args.get("location", 0))

    if start < 0:
        abort(400, "Invalid offset")

    if location not in LOCATIONS_AVAILABLE:
        abort(400, "Invalid location id")

    if start == 0:
        cached_data_item = app.cached_data.get(str(location))

        if cached_data_item and is_cache_fresh(cached_data_item.get("time")):
            return jsonify(cached_data_item.get("data"))

    cv_keskus = scraper.get_jobs_cv_keskus(start, location)
    cv = scraper.get_jobs_cv(start, location)

    combined = {"cv_keskus": cv_keskus, "cv": cv}

    if start == 0 and cv and cv_keskus:
        app.cached_data[str(location)] = {
            "data": combined,
            "time": time.time()
        }

    return jsonify(combined)


def is_cache_fresh(cache_time):
    return time.time() - cache_time < app.cache_lifespan


def initialise_logging():
    log_folder = os.path.join(os.getcwd(), 'logs')

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file = os.path.join(log_folder, "app.log")
    logging.basicConfig(filename=log_file, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


with app.app_context():
    initialise_logging()


if __name__ == '__main__':
    app.run()
