from flask import Flask, jsonify, request

import scraper
import time
import os
import logging

app = Flask(__name__)

app.cache_time = 1800
app.last_scrape_time = time.time() - app.cache_time
app.last_scrape_data = None


@app.route("/api/jobs", methods=['GET'])
def jobs_data():
    start = request.args.get("start", 0)

    if start == "0" and time.time() - app.last_scrape_time < app.cache_time:
        return jsonify(app.last_scrape_data)

    cv_keskus = scraper.get_jobs_cv_keskus(start)
    cv = scraper.get_jobs_cv(start)

    combined = {"cv_keskus": cv_keskus, "cv": cv}

    if start == "0" and cv and cv_keskus:
        app.last_scrape_time = time.time()
        app.last_scrape_data = combined

    return jsonify(combined)


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
