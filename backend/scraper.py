import logging
import requests
import timeConverter
import traceback
from bs4 import BeautifulSoup
from constants import LOCATIONS_CVK, LOCATIONS_CV


def get_jobs_cv_keskus(start, location):
    try:
        location = LOCATIONS_CVK.get(location)
        url = f'https://www.cvkeskus.ee/toopakkumised?op=search&search[job_salary]=3&ga_track=results&search[locations][]={location}&search[keyword]=&search[expires_days]=&search[job_lang]=&search[salary]=&dir=1&sort=activation_date'
        url = url + f'&start={start}' if start > 0 else url

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        jobs = soup.find(class_="jobs-list").find_all("a", class_="jobad-url")

        jobs_list = []

        for job in jobs:
            main_info = job.find("div", class_="main-info")

            time = main_info.find("div").find("span")
            position = main_info.find("h2")
            company = main_info.find(class_="job-company")
            salary = main_info.find(class_="salary-block")
            link = job.get("href")

            salary_text = salary.text.replace("\n", " ").replace("?", "€").replace(" ", "", 1)[:-1] if salary is not None else None
            link_text = "https://www.cvkeskus.ee" + link

            job_dict = {
                "position": position.text,
                "company": company.text,
                "time": timeConverter.convertCVKeskusToCVTimeFormat(time.text),
                "salary": salary_text,
                "link": link_text
            }

            jobs_list.append(job_dict)
        
        return jobs_list

    except Exception:
        traceback_str = traceback.format_exc()
        logging.error(f"CV Keskus:\n{traceback_str}")

        return []


def get_jobs_cv(start, location):
    try:
        location = LOCATIONS_CV.get(location)
        url = f"https://cv.ee/api/v1/vacancy-search-service/search?limit=30&offset={start}&towns[]={location}&fuzzy=true&suitableForRefugees=false&isHourlySalary=false&isRemoteWork=false&isQuickApply=false&sorting=LATEST&showHidden=true"
        response = requests.get(url)

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

        return []
