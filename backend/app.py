import logging
import os
import threading
import time
import traceback

from flask import Flask, jsonify, request, abort
from LocationHandler import LocationHandler
from RateLimiter import RateLimiter
from constants import LOCATIONS_AVAILABLE, CATEGORIES_AVAILABLE, ADS_LIMIT, LOCALHOST_IP, CACHE_LIFESPAN

app = Flask(__name__)
rate_limiter = RateLimiter()
location_handlers: dict[int, LocationHandler] = {location: LocationHandler() for location in LOCATIONS_AVAILABLE}


@app.route("/api/jobs", methods=['GET'])
def jobs_data():
    remote_ip = request.remote_addr
    real_ip = request.headers.get('X-Real-IP', None)
    start = int(request.args.get("start", 0))
    location = int(request.args.get("location", 0))
    category = int(request.args.get("category", 0))

    if remote_ip != LOCALHOST_IP or not real_ip:
        abort(403)

    if rate_limiter.is_limited(real_ip):
        abort(429, "Too many requests within a minute")
    else:
        rate_limiter.log_request(real_ip)

    if start < 0 or start % ADS_LIMIT != 0:
        abort(400, "Invalid offset")

    if location not in LOCATIONS_AVAILABLE:
        abort(400, "Invalid location id")

    if category not in CATEGORIES_AVAILABLE:
        abort(400, "Invalid category")

    try:
        jobs = location_handlers.get(location).get_jobs(start, location, category)
        return jsonify(jobs)
    except Exception:
        traceback_str = traceback.format_exc()
        logging.error(f"App Route:\n{traceback_str}")


def initialise_logging() -> None:
    log_folder = os.path.join(os.getcwd(), 'logs')

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file = os.path.join(log_folder, "app.log")
    logging.basicConfig(filename=log_file, level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')


def cleanup_location_handlers() -> None:
    while True:
        time.sleep(CACHE_LIFESPAN)
        print("Cleaning location handlers")
        for handler in location_handlers.values():
            handler.cleanup()


with app.app_context():
    initialise_logging()
    cleanup_thread = threading.Thread(target=cleanup_location_handlers, daemon=True)
    cleanup_thread.start()


if __name__ == '__main__':
    app.run()
