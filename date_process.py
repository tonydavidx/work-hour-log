from pandas import read_csv
import datetime


class DateProcess:
    def __init__(self):
        pass

    def get_last_run_date(self):
        data = read_csv('./data.csv')
        date = data['date'].iloc[-1]
        date = date.split('-')
        day = datetime.date(int(date[2]), int(date[1]), int(date[0]))
        return day
