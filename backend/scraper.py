import requests
from bs4 import BeautifulSoup


def get_jobs_cv_keskus(start):
    URL = 'https://www.cvkeskus.ee/toopakkumised?op=search&search%5Bjob_salary%5D=3&ga_track=all_ads&search%5Blocations%5D%5B%5D=4&search%5Bkeyword%5D=&dir=1&sort=activation_date'
    URL = URL + f'&start={start}' if start != 0 else URL

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    jobs = soup.find(class_="jobs-list").find_all("div", class_="main-info")

    jobs_list = []

    for job in jobs:
        link = job.find("a")
        time = job.find("div").find("span")
        position = job.find("h2")
        company = job.find(class_="job-company")
        salary = job.find(class_="salary-block")

        salary_text = salary.text.replace("\n", " ").replace("?", "€").replace(" ", "", 1)[:-1] if salary is not None else None
        link_text = "https://www.cvkeskus.ee" + link.get("href")

        job_dict = {
            "position": position.text,
            "company": company.text,
            "time": time.text,
            "salary": salary_text,
            "link": link_text
        }

        jobs_list.append(job_dict)

    return jobs_list


def get_jobs_cv():
    URL = 'https://cv.ee/api/v1/vacancy-search-service/search?limit=30&offset=0&towns[]=314&fuzzy=true&suitableForRefugees=false&isHourlySalary=false&isRemoteWork=false&isQuickApply=false&sorting=LATEST'
    response = requests.get(URL)

    if response.status_code == 200:
        jobs = response.json().get("vacancies", [])

        jobs_clean = []
        keys_to_keep = ["id", "positionTitle", "salaryFrom", "salaryTo", "hourlySalary", "publishDate", "employerName"]

        for job in jobs:
            job_clean = {key: job.get(key) for key in keys_to_keep}
            jobs_clean.append(job_clean)

        print(jobs_clean)
        return jobs_clean

    return []
