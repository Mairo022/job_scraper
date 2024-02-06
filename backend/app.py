from flask import Flask, jsonify, request

import scraper
import time

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

    if start == "0":
        app.last_scrape_time = time.time()
        app.last_scrape_data = combined

    return jsonify(combined)


if __name__ == '__main__':
    app.run()
