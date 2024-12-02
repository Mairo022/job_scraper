import logging
import requests
import traceback
from bs4 import BeautifulSoup
from constants import LOCATIONS_CVK, LOCATIONS_CV, ADS_LIMIT, CATEGORIES_CVK, CATEGORIES_CV
from scraperUtils import *


def get_jobs_cv_keskus(start, location, category):
    try:
        location = LOCATIONS_CVK.get(location)
        category = CATEGORIES_CVK.get(category)

        url = f'https://www.cvkeskus.ee/toopakkumised?op=search&search[job_salary]=3&ga_track=homepage&search[locations][]={location}&search[keyword]=&dir=1&sort=activation_date'
        url = url + f'&start={start}' if start > 0 else url
        url = url + f'&search[categories][]={category}' if category != 0 else url

        page = requests.get(url, timeout=5)
        soup = BeautifulSoup(page.content, "html.parser")
        jobs = soup.find(class_="jobs-list").find_all("a", class_="jobad-url")

        jobs_list = []

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

            job_dict = {
                "position": position.text,
                "company": company.text,
                "time": convertCVKeskusToCVTimeFormat(time_text),
                "salary": salary_text,
                "link": link_text
            }

            jobs_list.append(job_dict)
        
        return jobs_list

    except Exception:
        traceback_str = traceback.format_exc()
        logging.error(f"CV Keskus:\n{traceback_str}")
        print(traceback_str)

        return []


def get_jobs_cv(start, location, category):
    try:
        location = LOCATIONS_CV.get(location)
        category = CATEGORIES_CV.get(category)

        url = f"https://cv.ee/api/v1/vacancy-search-service/search?limit={ADS_LIMIT}&offset={start}&towns[]={location}&fuzzy=true&sorting=LATEST&showHidden=true"
        url = url + f'&categories[]={category}' if category != 0 else url

        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            jobs = response.json().get("vacancies", [])

            jobs_clean = []
            keys_to_keep = ["id", "positionTitle", "salaryFrom", "salaryTo", "hourlySalary", "publishDate", "employerName"]

            for job in jobs:
                job_clean = {key: job.get(key) for key in keys_to_keep}
                jobs_clean.append(job_clean)

            return jobs_clean

    except Exception:
        traceback_str = traceback.format_exc()
        logging.error(f"CV:\n{traceback_str}")
        print(traceback_str)

        return []
