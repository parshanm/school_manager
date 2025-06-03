from jdatetime import date as jdate
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtCore import QDate

class JalaliDateEdit(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCalendarPopup(True)
        self.setDisplayFormat("yyyy/MM/dd")
        self.setDate(QDate.currentDate())
        
    def date(self):
        """برگرداندن تاریخ به صورت شمسی"""
        qdate = super().date()
        jd = jdate.fromgregorian(
            year=qdate.year(),
            month=qdate.month(),
            day=qdate.day()
        )
        return jd
    
    def setJalaliDate(self, year, month, day):
        """تنظیم تاریخ با مقادیر شمسی"""
        gdate = jdate(year, month, day).togregorian()
        qdate = QDate(gdate.year, gdate.month, gdate.day)
        self.setDate(gdate)