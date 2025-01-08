from constants import ADS_LIMIT, LOCATIONS_CVK, CATEGORIES_CVK, LOCATIONS_CV, CATEGORIES_CV, LOCATIONS
from datetime import datetime, timezone, timedelta


def getTimeText(time, jobs, i) -> str:
    if time.split(" ")[-1] == "jäänud":
        i_change = 1 if (i == 0) else -1
        min_index = 0 if (i_change == 1) else 1

        while len(jobs) > i >= min_index:
            i += i_change
            job = jobs[i]
            main = job.find("div", class_="main-info")
            time_job = main.find("div").find_all("span")[-1].text

            if time_job.split(" ")[-1] != "jäänud":
                return time_job

    return time


def convertCVKeskusToCVTimeFormat(time_input: str) -> str:
    current_time = datetime.now(timezone.utc)
    time_split = time_input.split()

    final_time = ""

    if len(time_split) == 2:
        if time_split[0] == "päev":
            final_time = current_time - timedelta(days=1)
        elif time_split[0] == "tund":
            final_time = current_time - timedelta(hours=1)
        elif time_split[0] == "minut":
            final_time = current_time - timedelta(minutes=1)
        elif time_split[0] == "sekund":
            final_time = current_time - timedelta(seconds=1)
        elif time_split[0] == "nädal":
            final_time = current_time - timedelta(weeks=1)

    if len(time_split) == 3:
        if time_split[1] == "tundi":
            final_time = current_time - timedelta(hours=int(time_split[0]))
        elif time_split[1] == "min.":
            final_time = current_time - timedelta(minutes=int(time_split[0]))
        elif time_split[1] == "p.":
            final_time = current_time - timedelta(days=int(time_split[0]))
        elif time_split[1] == "näd.":
            final_time = current_time - timedelta(weeks=int(time_split[0]))
        elif time_split[1] == "s.":
            final_time = current_time - timedelta(seconds=int(time_split[0]))

    if isinstance(final_time, datetime):
        return final_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    return current_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')


def create_cvk_url(start, location, category) -> str:
    location = LOCATIONS_CVK.get(location)
    category = CATEGORIES_CVK.get(category)

    url = f'https://www.cvkeskus.ee/toopakkumised?op=search&search[job_salary]=3&ga_track=homepage&search[locations][]={location}&search[keyword]=&dir=1&sort=activation_date'
    url = url + f'&start={start}' if start > 0 else url
    url = url + f'&search[categories][]={category}' if category != 0 else url

    return url


def create_cv_url(start, location, category) -> str:
    # Load more ads when is Tallinn
    start += 30 if (location == LOCATIONS.TALLINN.value and start != 0) else 0
    ads_to_load = ADS_LIMIT if location != LOCATIONS.TALLINN.value else 60

    location = LOCATIONS_CV.get(location)
    category = CATEGORIES_CV.get(category)

    url = f"https://cv.ee/api/v1/vacancy-search-service/search?limit={ads_to_load}&offset={start}&towns[]={location}&fuzzy=true&sorting=LATEST&showHidden=true"
    url = url + f'&categories[]={category}' if category != 0 else url

    return url
