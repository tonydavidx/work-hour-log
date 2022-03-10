import requests
import os
import datetime
from datetime import date
from inputimeout import inputimeout, TimeoutOccurred

today = date.today()

endpoint = 'https://reports.api.clockify.me/v1'
workspace_id = '5e2a8dc28a512816cfa01c0d'
key = os.getenv('CLOCKIFY_KEY')
filters = {

    "dateRangeStart": f"{today}T00:00:00.000Z",
    "dateRangeEnd": f"{today}T23:59:59.999Z",
    "summaryFilter": {
        "groups": ["USER"],
    }
}


report = requests.post(f'{endpoint}/workspaces/{workspace_id}/reports/summary',
                       json=filters, headers={'X-Api-Key': key}).json()

worked_seconds = datetime.timedelta(
    seconds=report['totals'][0]['totalTime'])
# worked_seconds = datetime.timedelta(
#     seconds=45755)


hours_minutes = str(worked_seconds).split(':')
hours_minutes = hours_minutes[0] + '.' + hours_minutes[1]
print(hours_minutes)

with open('./data.csv', 'a') as f:
    f.write(f'{today},{hours_minutes}\n')
# user_input = input(
#     'Do you want to commit today (Y/N)\nignore or press Y to commit\npress N to stop script')
# # wait few seconds for input


def commit():
    os.system('git add .')
    # os.system(f'git commit -m "start"')
    os.system(f'git commit -m "Added workhours for {today} to data.csv"')
    os.system('git push')
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
