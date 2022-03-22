import random
from time import sleep, time
from pandas import read_csv
import requests
import os
import datetime
from datetime import date, timedelta
from inputimeout import inputimeout, TimeoutOccurred
from date_process import DateProcess

date_process = DateProcess()

os.chdir("D:/Documents/python/mini-projects/workhourlog")

LAST_RUN = date_process.get_last_run_date()
print(LAST_RUN)
date_process.get_today_date()
endpoint = "https://reports.api.clockify.me/v1"
workspace_id = "5e2a8dc28a512816cfa01c0d"
key = os.getenv("CLOCKIFY_KEY")
days_not_recorded = date_process.get_range_value()

if LAST_RUN is None:
    day = datetime.date(2021, 12, 31)
else:
    day = LAST_RUN

for i in range(days_not_recorded):
    day = day + timedelta(days=1)
    filters = {
        "dateRangeStart": f"{day}T00:00:00.000Z",
        "dateRangeEnd": f"{day}T23:59:59.999Z",
        "summaryFilter": {
            "groups": ["USER"],
        },
    }

    report = requests.post(
        f"{endpoint}/workspaces/{workspace_id}/reports/summary",
        json=filters,
        headers={"X-Api-Key": key},
    ).json()
    try:
        worked_seconds = datetime.timedelta(seconds=report["totals"][0]["totalTime"])

    except Exception:
        worked_seconds = datetime.timedelta(seconds=0)

    hours_minutes = str(worked_seconds).split(":")
    hours_minutes = hours_minutes[0] + "." + hours_minutes[1]
    print(f"{day} - {hours_minutes}")
    str_date = day.strftime("%d-%m-%Y")
    with open("D:\Documents\python\mini-projects\workhourlog\data.csv", "a") as f:
        f.write(f"{str_date},{hours_minutes}")

    sleep(random.randint(1, 3))


def commit():
    os.system("git add .")
    os.system(f'git commit -m "Added workhours for {str_date} to data.csv"')
    os.system("git push -f")
    print("done")


try:
    user_input = inputimeout("want to commit (Y/N)", timeout=5)
    if user_input.lower() == "y":
        commit()
    if user_input.lower() == "n":
        print("no commits today")

except TimeoutOccurred:
    print("timeout occured going to commit")
    commit()
