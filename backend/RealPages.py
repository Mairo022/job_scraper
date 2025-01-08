import time
from typing import List

from constants import ADS_LIMIT, CACHE_LIFESPAN, LOCATIONS_AVAILABLE


class _Pages:
    def __init__(self, location_id):
        self.pages = {0: {'cv': 0, 'cvk': 0}}
        self.last_updated = time.time()
        self.location_id = location_id

    def get_pages(self, offset) -> List:
        current_pages = self.pages.get(offset)
        previous_pages = self.pages.get(offset-ADS_LIMIT)

        if not self.__is_fresh():
            return [offset, offset]

        if current_pages:
            return [current_pages.get("cv"), current_pages.get("cvk")]

        if previous_pages:
            previous_cv = previous_pages.get("cv")
            previous_cvk = previous_pages.get("cvk")

            current_cv = previous_cv if previous_cv + ADS_LIMIT != offset else offset
            current_cvk = previous_cvk if previous_cvk + ADS_LIMIT != offset else offset

            return [current_cv, current_cvk]

        return [offset, offset]

    def set_pages(self, offset, offset_cv, offset_cvk, cv_ads_older, cvk_ads_older):
        current_pages = self.pages.get(offset)
        next_offset = offset + ADS_LIMIT

        if current_pages:
            current_cv = current_pages.get("cv")
            current_cvk = current_pages.get("cvk")

            if cvk_ads_older:
                self.pages[next_offset] = {"cv": current_cv + ADS_LIMIT, "cvk": current_cvk}
            elif cv_ads_older:
                self.pages[next_offset] = {"cv": current_cv, "cvk": current_cvk + ADS_LIMIT}
            else:
                self.pages[next_offset] = {"cv": current_cv + ADS_LIMIT, "cvk": current_cvk + ADS_LIMIT}

        if not current_pages:
            if cv_ads_older:
                self.pages[next_offset] = {"cv": offset_cv, "cvk": next_offset}
            elif cvk_ads_older:
                self.pages[next_offset] = {"cv": next_offset, "cvk": offset_cvk}
            else:
                self.pages[next_offset] = {"cv": next_offset, "cvk": next_offset}

        self.last_updated = time.time()

    def __is_fresh(self) -> bool:
        return time.time() - self.last_updated < CACHE_LIFESPAN


class RealPages:
    def __init__(self):
        self.pages = dict()
        for location in LOCATIONS_AVAILABLE:
            self.pages[location] = _Pages(location)
