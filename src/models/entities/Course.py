"""Course Module"""
from utils.DateFormat import DateFormat
from flask_restx import fields, Namespace


class Course():

    def __init__(self, id, name=None, credits=None, beginDate=None) -> None:
        self.id = id
        self.name = name
        self.credits = credits
        self.beginDate = beginDate
        

    def to_JSON(self):
        return {
            'id': self.id,
            'name': self.name,
            'credits': self.credits,
            'beginDate': DateFormat.convert_date(self.beginDate)
        }
#