from datetime import datetime, timedelta
from typing import TypedDict, Optional

import scraper
from constants import CACHE_LIFESPAN, ADS_LIMIT, CATEGORIES


class LocationHandler:
    def __init__(self):
        self.cache_cv: dict[int, "_Jobs"] = dict()
        self.cache_cvk: dict[int, "_Jobs"] = dict()
        self.leftovers_cv: dict[int, "_Jobs"] = dict()
        self.leftovers_cvk: dict[int, "_Jobs"] = dict()

    def get_jobs(self, start: int, location: int, category: int) -> dict[str, list]:
        if CATEGORIES.ALL.value != category:
            return {
                "cv": scraper.get_jobs_cv(start, location, category),
                "cv_keskus": scraper.get_jobs_cv_keskus(start, location, category)
            }

        cached_cv = self._get_cached_jobs("cv", start)
        cached_cvk = self._get_cached_jobs("cvk", start)

        if are_jobs_cached := cached_cv is not None and cached_cvk is not None:
            return {"cv": cached_cv, "cv_keskus": cached_cvk}

        cv = scraper.get_jobs_cv(start, location, category)
        cvk = scraper.get_jobs_cv_keskus(start, location, category)

        self._handle_request_data(cv, cvk, start)

        cv = self.cache_cv.get(start).get("jobs")
        cvk = self.cache_cvk.get(start).get("jobs")

        return {"cv": cv, "cv_keskus": cvk}

    def _handle_request_data(self, cv: list, cvk: list, start: int) -> None:
        cv_leftovers = self._get_leftover_jobs("cv", start)
        cvk_leftovers = self._get_leftover_jobs("cvk", start)

        cv = cv_leftovers + cv
        cvk = cvk_leftovers + cvk

        leftovers_site, leftovers = self._find_leftovers(cv, cvk)

        if leftovers_site == "cv":
            cv = cv[:-len(leftovers)]

        if leftovers_site == "cvk":
            cvk = cvk[:-len(leftovers)]

        if is_site_behind := len(leftovers) == ADS_LIMIT and start != 0:
            if is_behind_twice_in_a_row := leftovers_site == "cv" and len(cv_leftovers) == ADS_LIMIT:
                self._delete_leftover(leftovers_site, start - 30)

            if is_behind_twice_in_a_row := leftovers_site == "cvk" and len(cvk_leftovers) == ADS_LIMIT:
                self._delete_leftover(leftovers_site, start - 30)

        self._set_leftovers(leftovers_site, leftovers, start)
        self._set_cache("cv", cv, start)
        self._set_cache("cvk", cvk, start)
        self._delete_above_cache(start)

    @staticmethod
    def _find_leftovers(cv: list, cvk: list) -> tuple[Optional[str], list]:
        len_cv = len(cv)
        len_cvk = len(cvk)

        if has_no_leftovers := (len_cv == 0 or len_cvk == 0):
            return None, []

        cv_time = datetime.strptime(cv[len_cv-1].get("publishDate"), "%Y-%m-%dT%H:%M:%S.%f%z")
        cvk_time = datetime.strptime(cvk[len_cvk-1].get("time"), "%Y-%m-%dT%H:%M:%S.%f%z")

        leftovers_site = "cvk" if cv_time > cvk_time else "cv"
        leftovers = []

        if leftovers_site == "cv":
            for i in reversed(range(len_cv)):
                cv_time = datetime.strptime(cv[i].get("publishDate"), "%Y-%m-%dT%H:%M:%S.%f%z")

                if cv_is_older := cv_time < cvk_time:
                    leftovers.append(cv[i])
                    continue
                break

        if leftovers_site == "cvk":
            for i in reversed(range(len_cvk)):
                cvk_time = datetime.strptime(cvk[i].get("time"), "%Y-%m-%dT%H:%M:%S.%f%z")

                if cvk_is_older := cvk_time < cv_time:
                    leftovers.append(cvk[i])
                    continue
                break

        leftovers.reverse()

        return leftovers_site, leftovers

    def _set_leftovers(self, site: str, ads: list, start: int) -> None:
        if site == "cv":
            self.leftovers_cv[start] = {"jobs": ads, "valid_until": self._create_valid_until_time()}
        if site == "cvk":
            self.leftovers_cvk[start] = {"jobs": ads, "valid_until": self._create_valid_until_time()}

    def _get_leftover_jobs(self, site: str, start: int) -> list:
        if start == 0:
            return []

        start = start - ADS_LIMIT
        leftover = self._get_leftover(site, start)

        return leftover.get("jobs") if (leftover is not None) else []

    def _get_leftover(self, site: str, start: int) -> "_Jobs":
        if site == "cv":
            return self.leftovers_cv.get(start)
        else:
            return self.leftovers_cvk.get(start)

    def _delete_leftover(self, site: str, start: int) -> None:
        if site == "cv":
            del self.leftovers_cv[start]
        if site == "cvk":
            del self.leftovers_cvk[start]

    def _set_cache(self, site: str, jobs: list, start: int) -> None:
        if site == "cv":
            self.cache_cv[start] = {"jobs": jobs, "valid_until": self._create_valid_until_time()}
        if site == "cvk":
            self.cache_cvk[start] = {"jobs": jobs, "valid_until": self._create_valid_until_time()}

    def _get_cached_jobs(self, site: str, start: int) -> Optional[list]:
        cached = self._get_cached(site, start)

        if cached is None:
            return None

        if is_valid := datetime.now() < cached.get("valid_until"):
            return cached.get("jobs")
        else:
            self._delete_from_cache(site, start)
            return None

    def _get_cached(self, site: str, start: int) -> Optional["_Jobs"]:
        if site == "cv":
            return self.cache_cv.get(start)
        else:
            return self.cache_cvk.get(start)

    def _delete_above_cache(self, start: int) -> None:
        start = start + ADS_LIMIT
        if self.cache_cv.get(start) and self.cache_cvk.get(start):
            self._delete_from_cache("cv", start)
            self._delete_from_cache("cvk", start)

    def _delete_from_cache(self, site: str, start: int) -> None:
        if site == "cv":
            del self.cache_cv[start]
        if site == "cvk":
            del self.cache_cvk[start]

    @staticmethod
    def _create_valid_until_time() -> datetime:
        return datetime.now() + timedelta(seconds=CACHE_LIFESPAN)

    def cleanup(self) -> None:
        now = datetime.now()

        cv_caches_to_delete = [key for key, cache in self.cache_cv.items() if now > cache.get("valid_until")]
        cv_lo_to_delete = [key for key, leftover in self.leftovers_cv.items() if now > leftover.get("valid_until")]
        cvk_caches_to_delete = [key for key, cache in self.cache_cvk.items() if now > cache.get("valid_until")]
        cvk_lo_to_delete = [key for key, leftover in self.leftovers_cvk.items() if now > leftover.get("valid_until")]

        for key in cv_caches_to_delete: del self.cache_cv[key]
        for key in cv_lo_to_delete: del self.leftovers_cv[key]
        for key in cvk_caches_to_delete: del self.cache_cvk[key]
        for key in cvk_lo_to_delete: del self.leftovers_cvk[key]


class _Jobs(TypedDict):
    jobs: list
    valid_until: datetime
