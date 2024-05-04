from constants import ADS_LIMIT
from datetime import datetime, timezone, timedelta


def getTimeText(time, jobs, i):
    if time.split(" ")[-1] == "jäänud":
        if i == 0:
            job = jobs[i+1]
            main_info = job.find("div", class_="main-info")
            time = main_info.find("div").find_all("span")[-1]

            return time.text
        if i <= ADS_LIMIT:
            job = jobs[i-1]
            main_info = job.find("div", class_="main-info")
            time = main_info.find("div").find_all("span")[-1]

            return time.text

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