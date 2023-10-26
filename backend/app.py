from flask import Flask, jsonify, request
import scraper

app = Flask(__name__)


@app.route("/api/jobs", methods=['GET'])
def jobs_data():
    start = request.args.get("start", 0)

    cv_keskus = scraper.get_jobs_cv_keskus(start)
    cv = scraper.get_jobs_cv(start)

    combined = {"cv_keskus": cv_keskus, "cv": cv}

    return jsonify(combined)


if __name__ == '__main__':
    app.run()
