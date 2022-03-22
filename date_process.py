from pandas import read_csv
import datetime


class DateProcess:
    def __init__(self):
        pass

    def get_last_run_date(self):
        data = read_csv('D:/Documents/python/mini-projects/workhourlog/data.csv')
        date = data['date'].iloc[-1]
        date = date.split('-')
        day = datetime.date(int(date[2]), int(date[1]), int(date[0]))
        return day

    def get_today_date(self):
        today = datetime.date.today()
        return today

    def get_range_value(self):
        today = self.get_today_date()
        last_run = self.get_last_run_date()
        range_value = today - last_run
        days = range_value.days
        return days


if __name__ == '__main__':
    date_process = DateProcess()
