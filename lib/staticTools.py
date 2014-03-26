from lib.header import *
from PyQt4 import QtGui  
class maths:
    @staticmethod
    def rounder(nr):
        origNr = nr
        intNr = int(nr)
        afterComma = nr - intNr
        stringComma = str(afterComma)
        if len(stringComma) >= 5:
            stringComma = str(abs(float(stringComma)))
            if int(stringComma[4:5]) > 5:
                correctAfterComma = int(stringComma[2:3]) + 1
            else:
                correctAfterComma = int(stringComma[2:3]) 
            floatString = str(intNr)+"."+str(correctAfterComma)
            return floatString
        else:
            return str(origNr)
    
    @staticmethod
    def calcJobSum(company,  job, workCalendar):
        daySpace,  weekendPart = sdt.calcDaySpace(job.startdate, job.enddate, workCalendar,  job.weekendDays)
        hrSpace = daySpace * job.hours + job.correctionHours
        chargeSum = 0
        for charge in job.wcharges:
            if charge.howManyTimes == 0:
                chargeValue = daySpace * charge.value
            else:
                chargeValue = charge.howManyTimes * charge.value
            chargeSum += chargeValue
        loanDistractionSum = 0
        for loanDistraction in company.loanDistractions:
            if loanDistraction.money:
                loanDistractionSum += loanDistraction.value
            else:
                loanDistractionSum += (company.loan / 100) * loanDistraction.value
        realHourLoan = (company.loan - loanDistractionSum) 
        realHourSplitSum= loanDistractionSum * (hrSpace / company.perHours)
        loanSum = realHourLoan * (hrSpace / company.perHours) + chargeSum
        return  (loanSum,  loanDistractionSum, realHourLoan, realHourSplitSum,  chargeSum)

#cw = condition-wrapper
class cw:
    @staticmethod
    def checkForValidDate(startdate, enddate,  wCalendarDate):
        return (startdate.month() == wCalendarDate.month() and startdate.year() == wCalendarDate.year()) or (enddate.month() == wCalendarDate.month() and startdate.year() == wCalendarDate.year())
    def filterTextSearch(infoSearch,  job,  company):
        return (re.search(infoSearch,  job.name.lower()) is not None  or re.search(infoSearch,  job.place.lower()) is not None or re.search(infoSearch,  job.comment.lower()) is not None or re.search(infoSearch,  job.leader.lower()) is not None or re.search(infoSearch, company.name.lower()) is not None)
    @staticmethod
    def ifInsertPersonalFinance(ui,  pf):
        pfCal = QtCore.QDate.fromString(str(ui.pfCalendar.monthShown())+"."+str(ui.pfCalendar.yearShown()), "M.yyyy")
        pfSearch = ui.pfSearch.text()
        pfSearch = pfSearch.lower()
        if ui.pfCalendarEnabled.isChecked() == False and ui.pfSearchEnabled.isChecked()==False:
            return True
        elif ui.pfCalendarEnabled.isChecked() and ui.pfSearchEnabled.isChecked()==False:
            if pf.date.month() == pfCal.month() and pf.date.year() == pfCal.year():
                return True
        elif  ui.pfCalendarEnabled.isChecked() == False and  ui.pfSearchEnabled.isChecked():
            if ui.pfSearch.text() == "":
                return True
            elif re.search(pfSearch,  pf.name.lower()) is not None:
                return True
        elif ui.pfCalendarEnabled.isChecked() and ui.pfSearchEnabled.isChecked():
            if ui.pfSearch.text() == "" and  (pf.date.month() == pfCal.month() and pf.date.year() == pfCal.year()):
                return True
            elif re.search(pfSearch,  pf.name.lower()) is not None  and  (pf.date.month() == pfCal.month() and pf.date.year() == pfCal.year()):
                return True
        else:
            return False
    @staticmethod
    def insertJobYesNo(ui, company, job, infoSearch, workCalendar):
        insertARow = False
        if ui.filterAll.isChecked():
            #cal + search
            if ui.filterCalendar.isChecked() and ui.filterInactive.isChecked() and infoSearch != "":
                if cw.checkForValidDate(job.startdate, job.enddate, workCalendar) and  cw.filterTextSearch(infoSearch, job, company):
                    #(ui,  job, company, rowNr,  daySpace, singleView, sum)
                    insertARow = True
            #cal +inactive + search
            if ui.filterCalendar.isChecked() and ui.filterInactive.isChecked() == False and infoSearch != "":
                if cw.checkForValidDate(job.startdate, job.enddate, workCalendar) and cw.filterTextSearch(infoSearch, job, company) and job.active == 1:
                    insertARow = True
            #search
            elif ui.filterCalendar.isChecked() == False and ui.filterInactive.isChecked() and infoSearch != "":
                if cw.filterTextSearch(infoSearch, job, company):
                    insertARow = True
            #----- no filters (but filter@all)
            elif ui.filterCalendar.isChecked() == False and ui.filterInactive.isChecked() and infoSearch == "": 
                insertARow = True
            #calendar
            elif ui.filterCalendar.isChecked() and ui.filterInactive.isChecked() and infoSearch == "":
                if cw.checkForValidDate(job.startdate, job.enddate, workCalendar):
                    insertARow = True
            #inactive calendar
            elif ui.filterCalendar.isChecked() and ui.filterInactive.isChecked() == False and infoSearch == "":
                if cw.checkForValidDate(job.startdate, job.enddate, workCalendar) and job.active == 1:
                    insertARow = True
            #inactive
            elif ui.filterCalendar.isChecked() ==False and ui.filterInactive.isChecked() == False and infoSearch == "":
                if  job.active == 1:
                    insertARow = True
            #inactive + search
            elif ui.filterCalendar.isChecked() ==False and ui.filterInactive.isChecked() == False and infoSearch != "":
                if  cw.filterTextSearch(infoSearch, job, company) and job.active == 1:
                    insertARow = True
        else:
            insertARow = True
        return insertARow
