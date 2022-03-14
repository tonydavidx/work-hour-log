from time import sleep, time
from types import NoneType
import requests
import os
import datetime
from datetime import date, timedelta
from inputimeout import inputimeout, TimeoutOccurred

LAST_RUN = None

endpoint = 'https://reports.api.clockify.me/v1'
workspace_id = '5e2a8dc28a512816cfa01c0d'
key = os.getenv('CLOCKIFY_KEY')

if LAST_RUN is None:
    day = datetime.date(2021, 12, 31)
else:
    day = LAST_RUN

# for i in range(3):
day = day + timedelta(days=1)
filters = {
    "dateRangeStart": f"{day}T00:00:00.000Z",
    "dateRangeEnd": f"{day}T23:59:59.999Z",
    "summaryFilter": {
        "groups": ["USER"],
    }
}

report = requests.post(f'{endpoint}/workspaces/{workspace_id}/reports/summary',
                       json=filters, headers={'X-Api-Key': key}).json()
print(report)
try:
    worked_seconds = datetime.timedelta(
        seconds=report['totals'][0]['totalTime'])

except Exception:
    worked_seconds = datetime.timedelta(seconds=0)

hours_minutes = str(worked_seconds).split(':')
hours_minutes = hours_minutes[0] + '.' + hours_minutes[1]
print(hours_minutes)
str_date = day.strftime('%d-%m-%Y')
with open('./data.csv', 'a') as f:
    f.write(f'{str_date},{hours_minutes}\n')

sleep(1)


def commit():
    os.system('git add .')
    os.system(f'git commit -m "Added workhours for {str_date} to data.csv"')
    os.system('git push -f')
    print('done')


try:
    user_input = inputimeout('want to commit (Y/N)', timeout=5)
    if user_input.lower() == 'y':
        commit()
    if user_input.lower() == 'n':
        print('no commits today')

except TimeoutOccurred:
    print('timeout')
    commit()
