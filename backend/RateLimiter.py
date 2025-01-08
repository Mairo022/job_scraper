import time
from collections import Counter

from constants import MAX_REQUESTS_PER_MIN_BY_IP


class RateLimiter:
    updated_at = time.time()
    requests = Counter()  # key: ip, value: requests amount

    def log_request(self, ip):
        ip = ip.strip()
        self.requests[ip] += 1

    def is_limited(self, ip) -> bool:
        ip = ip.strip()
        now = time.time()
        is_requests_minute_old = now - self.updated_at > 60

        if is_requests_minute_old:
            self.requests.clear()
            self.updated_at = now
            return False

        return self.requests[ip] >= MAX_REQUESTS_PER_MIN_BY_IP
