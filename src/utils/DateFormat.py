import datetime

class DateFormat():

    @classmethod
    def convert_date(self, date):
        # return datetime.datetime.strftime(date, '%Y/%m/%d/')
        formatedDate = date.isoformat()
        return formatedDate
