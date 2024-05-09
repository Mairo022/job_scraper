from flask import Flask, jsonify, request, abort

from appUtils import *
from constants import LOCATIONS_AVAILABLE, ADS_LIMIT


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

    job_ads = get_jobs(start, location, app.cached_data, app.real_pages[location])

    return jsonify(job_ads)


with app.app_context():
    initialise_logging()


if __name__ == '__main__':
    app.run()
