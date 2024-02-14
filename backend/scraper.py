import logging
import requests
import timeConverter
import traceback
from bs4 import BeautifulSoup

def get_jobs_cv_keskus(start):
    try:
        URL = 'https://www.cvkeskus.ee/toopakkumised?op=search&search%5Bjob_salary%5D=3&ga_track=all_ads&search%5Blocations%5D%5B%5D=4&search%5Bkeyword%5D=&dir=1&sort=activation_date'
        URL = URL + f'&start={start}' if int(start) > 0 else URL

        page = requests.get(URL)

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


def get_jobs_cv(start):
    try:
        URL = f'https://cv.ee/api/v1/vacancy-search-service/search?limit=30&offset={start}&towns[]=314&fuzzy=true&suitableForRefugees=false&isHourlySalary=false&isRemoteWork=false&isQuickApply=false&sorting=LATEST'

        response = requests.get(URL)

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
