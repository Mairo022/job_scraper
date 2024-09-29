from flask import Flask, jsonify, request, abort

from RateLimiter import RateLimiter
from appUtils import *
from constants import LOCATIONS_AVAILABLE, CATEGORIES_AVAILABLE, ADS_LIMIT, LOCALHOST_IP

app = Flask(__name__)

app.cached_data = dict()
app.real_pages = initialise_pages()
app.rate_limiter = RateLimiter()


@app.route("/api/jobs", methods=['GET'])
def jobs_data():
    remote_ip = request.remote_addr
    real_ip = request.headers.get('X-Real-IP', None)
    start = int(request.args.get("start", 0))
    location = int(request.args.get("location", 0))
    category = int(request.args.get("category", 0))

    if remote_ip != LOCALHOST_IP or not real_ip:
        abort(403)

    if app.rate_limiter.is_limited(real_ip):
        abort(429, "Too many requests within a minute")
    else:
        app.rate_limiter.log_request(real_ip)

    if start < 0 or start % ADS_LIMIT != 0:
        abort(400, "Invalid offset")

    if location not in LOCATIONS_AVAILABLE:
        abort(400, "Invalid location id")

    if category not in CATEGORIES_AVAILABLE:
        abort(400, "Invalid category")

    job_ads = get_jobs(start, location, app.cached_data, app.real_pages[location], category)

    return jsonify(job_ads)


with app.app_context():
    initialise_logging()


if __name__ == '__main__':
    app.run()
