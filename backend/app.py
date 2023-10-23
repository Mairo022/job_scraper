from flask import Flask, jsonify
import scraper

app = Flask(__name__)


@app.route("/api/jobs", methods=['GET'])
def jobs_data():
    cv_keskus = scraper.get_jobs_cv_keskus(0)
    cv = scraper.get_jobs_cv()

    combined = {"cv_keskus": cv_keskus, "cv": cv}

    return jsonify(combined)


if __name__ == '__main__':
    app.run()
