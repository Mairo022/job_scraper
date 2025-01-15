import logging
from typing import TypedDict

import requests
import traceback
from bs4 import BeautifulSoup
from scraperUtils import *


def get_jobs_cv_keskus(start: int, location: int, category: int) -> list["_CvkJobs"]:
    jobs_clean: list[_CvkJobs] = []

    try:
        url = create_cvk_url(start, location, category)

        page = requests.get(url, timeout=5)

        if page.status_code != 200:
            raise Exception(f"CVK response code != 200, is: {page.status_code}")

        soup = BeautifulSoup(page.content, "html.parser")
        jobs = soup.find(class_="jobs-list").find_all("a", class_="jobad-url")

        for i, job in enumerate(jobs):
            main_info = job.find("div", class_="main-info")

            time = main_info.find("div").find_all("span")[-1]
            position = main_info.find("h2")
            company = main_info.find(class_="job-company")
            salary = main_info.find(class_="salary-block")
            link = job.get("href")

            time_text = getTimeText(time.text, jobs, i)
            salary_text = salary.text.rsplit("\xa0", 1)[0] if salary is not None else None
            link_text = "https://www.cvkeskus.ee" + link

            job_dict: _CvkJobs = {
                "position": position.text,
                "company": company.text,
                "time": convertCVKeskusToCVTimeFormat(time_text),
                "salary": salary_text,
                "link": link_text
            }

            jobs_clean.append(job_dict)

    except Exception:
        traceback_str = traceback.format_exc()
        logging.error(f"CV Keskus:\n{traceback_str}")
        print(traceback_str)
        jobs_clean.clear()

    finally:
        return jobs_clean


def get_jobs_cv(start: int, location: int, category: int) -> list["_CvJobs"]:
    jobs_clean: list[_CvJobs] = []

    try:
        url = create_cv_url(start, location, category)

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            raise Exception(f"CV response code != 200, is: {response.status_code}")

        jobs = response.json().get("vacancies", [])
        keys_to_keep = _CvJobs.__annotations__.keys()

        for job in jobs:
            job_clean: _CvJobs = {key: job.get(key) for key in keys_to_keep}
            jobs_clean.append(job_clean)

    except Exception:
        traceback_str = traceback.format_exc()
        logging.error(f"CV:\n{traceback_str}")
        print(traceback_str)
        jobs_clean.clear()

    finally:
        return jobs_clean


class _CvJobs(TypedDict):
    id: int
    positionTitle: str
    salaryFrom: int | None
    salaryTo: int | None
    hourlySalary: bool
    publishDate: str
    employerName: str


class _CvkJobs(TypedDict):
    position: str
    company: str
    time: str
    salary: str | None
    link: str
