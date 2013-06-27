from header import *

def tr(name):
    return QtCore.QCoreApplication.translate("@default",  name)
#semantic designer tools
class sdt:

    @staticmethod
    def tB(text):
        alertBox = QtGui.QInputDialog.getText(ui,  text, text)
#        alertBox.setInputMode(QtGui.QInputDialog.TextInput)
#        alertBox.setText(text)
#        alertBox.exec()

    @staticmethod
    def aB(text):
        alertBox = QtGui.QMessageBox()
        alertBox.setText(text)
        alertBox.exec()
    
    @staticmethod
    def calcDaySpace(startdate,  enddate,  wc,  weekendDays):
        if startdate.daysTo(enddate) == 0:
            daySpace = 1
        elif startdate.month() != enddate.month():
            allDays = startdate.daysTo(enddate)
            if startdate.month() == wc.month():
                daySpace = allDays - enddate.day()+1
            else:
                daySpace = allDays - (startdate.daysInMonth() - startdate.day())
        else:
                daySpace = startdate.daysTo(enddate) + 1
        weekendPart = int(daySpace / 7) * weekendDays
        daySpace = daySpace - weekendPart
        return (daySpace,  weekendPart)
    @staticmethod
    def createJobRow(ui,  job, company, workCalendar,  rowNr, sum):
        colNr = 0
        if not singleView:
            daySpace,  weekendPart = sdt.calcDaySpace(job.startdate,  job.enddate, workCalendar,  job.weekendDays)
        else:
            daySpace,  weekendPart = (dater.daysInMonth() - (job.weekendDays * 4), job.weekendDays)
        #minSpace = daySpace * job.hours * 60
        loanSum,  loanSplitSum, realHourLoan, realHourSplitSum,  chargeSum = maths.calcJobSum(company,  job,  workCalendar)
        #building table..
        if not singleView:
            w = QtGui.QTableWidgetItem(str(company.name))
            w.setToolTip(company.describtion)
            ui.infoExel.setItem(rowNr,  colNr,   w)
            colNr = colNr + 1
        w = QtGui.QTableWidgetItem(job.name)
        w.setToolTip(job.comment)
        ui.infoExel.setItem(rowNr,  colNr,   w)
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(job.place) ))
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(job.leader) ))
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(sdt.rounder(loanSum) + ".- ("+sdt.rounder(realHourLoan)+"/std)" ))
        colNr = colNr + 1
        w = QtGui.QTableWidgetItem(sdt.rounder(daySpace * job.hours) +" Std")
        w.setToolTip(tr("From ")+job.startdate.toString(dbDateFormat)+" to "+job.enddate.toString(dbDateFormat)+ " AND <br />"+sdt.rounder(daySpace)+ "d (*"+str(job.hours)+"h)+"+str(weekendPart)+" Weekenddays")
        ui.infoExel.setItem(rowNr,  colNr,   w)
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(sdt.rounder(chargeSum)+".- " ))
        colNr = colNr + 1
        w = QtGui.QTableWidgetItem(sdt.rounder(realHourSplitSum)+".- @all")
        w.setToolTip(sdt.rounder(loanSplitSum)+".-/"+str(company.perHours)+tr("h")+")")
        ui.infoExel.setItem(rowNr,  colNr,   w)
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(sdt.rounder(sum + loanSum)+".-" ))
        return loanSum
    @staticmethod
    def colorChanger(color):
        if color > 200:
            return 25
        else:
            return color + 53
    @staticmethod
    def updateGraphicView(ui, companyList, workCalendar, infoSearch):
        pen= QtGui.QPen(QtCore.Qt.red)
        r, g, b=(233, 36, 99)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setWidth(4)
        widthPerHour = 1.15
        scene = QtGui.QGraphicsScene()
        #lastLine = 0
        oldDaySpace = 0.00
        oldValue = 0.00
        allValue = 0
        for company in companyList:
            for job in company.jobs:
                if cw.insertJobYesNo(ui, company, job, infoSearch, workCalendar):
                    daySpace,  weekendPart = sdt.calcDaySpace(job.startdate, job.enddate, workCalendar,  job.weekendDays)
                    loanSum,  loanSplitSum, realHourLoan,  realHourSplitSum,  chargeSum = maths.calcJobSum(company,  job,  workCalendar)
                    daySpace = ((daySpace * job.hours) + job.correctionHours )
                    daySpace = (daySpace + oldDaySpace) 
                    value = ((company.loan/10)*daySpace)
                    allValue += value
                    #print(job.name+"="+str(value)+":"+str(daySpace))
                    scene.addLine(float(oldDaySpace),float(-oldValue) ,   float(daySpace*widthPerHour), float(-loanSum/50),  pen)
                    oldDaySpace = daySpace*widthPerHour
                    oldValue = loanSum/50
                    r=sdt.colorChanger(r)
                    g=sdt.colorChanger(g)
                    b=sdt.colorChanger(b)
                    pen.setColor(QtGui.QColor(r, g, b))
        ui.graphView.setScene(scene)
    @staticmethod
    def createDetailText(company, workCalendar, cvCalIsChecked):
        text = ""
        text += "<h1>"+company.name+"</h1>"+company.describtion+"<br />"+tr("Loan")+": "+str(company.loan)+" (per "+str(company.perHours)+tr("h")+")<hr />"
        loanSplitSum = 0
        #LoanSplits
        text += "<h4>"+tr("LoanSplits")+"</h4><ul>"
        for ls in  company.loanSplits:
            text += "<li>"+ls.name+": "+str(ls.value)
            if ls.money:
                loanSplitSum += ls.value
                text += ".- </li>"
            else:
                inMoney = (company.loan / 100) * ls.value
                loanSplitSum += inMoney
                text += "% ("+sdt.rounder(inMoney)+".-) </li>"
        text += "</ul>"
        if loanSplitSum > 0:
            text += tr("Loansplitsum")+": "+sdt.rounder(loanSplitSum)+".-/"+str(company.perHours)+" "+tr("h")+"<hr />"
        creditSum = 0
        text += "<h4>"+tr("Credits")+"</h4><ul><pre>"
        for credit in company.credits:
            if (credit.date.month() == workCalendar.month() and credit.date.year() == workCalendar.year()) or True is not cvCalIsChecked:
                creditSum += credit.value
                text += "<li>"+credit.date.toString(dbDateFormat) + ": "+str(credit.value)+""
                if credit.payed:
                    text +=".-      "+ tr("is")+" "+tr("payed")+"</li>"
                else:
                    text +=".-      "+ tr("is NOT")+" "+tr("payed")+"</li>"
        text += "</ul></pre>"
        if creditSum > 0:
            text += tr("Creditsum")+": "+sdt.rounder(creditSum)+".- <hr />"
        jobSum = 0
        jobDays = 0
        jobHours = 0

        chargeSum = 0
        text += "<h4>"+tr("Jobs")+"</h4>"
        text += "<ul>"
        for job in company.jobs:
            if cvCalIsChecked:
                if cw.checkForValidDate(job.startdate, job.enddate, workCalendar):
                    days,  weekendPart = sdt.calcDaySpace(job.startdate,  job.enddate, workCalendar,  job.weekendDays)
                else:
                    days = -1
            else:
                days = job.startdate.daysTo(job.enddate) + 1
            if days != -1:
                jobDays += days
                hourSpace = days * (job.hours / company.perHours ) +job.correctionHours
                jobHours += hourSpace
                jobSum += company.loan * hourSpace
                text += "<li>"+job.name+": "+sdt.rounder(days)+"d * ("+sdt.rounder(job.hours)+"h /"+str(company.perHours)+" )+" +str(job.correctionHours)+"h = "+sdt.rounder(hourSpace)+"h * " + str(company.loan)+".-  ="+sdt.rounder(hourSpace*company.loan)+".- </li>"
                text += "<ul>"
                for charge in job.wcharges:
                    if charge.howManyTimes > 0:
                        chargeSum += charge.value * charge.howManyTimes
                        text += "<li><pre>"+charge.name+": "+str(charge.value)+".- * "+str(charge.howManyTimes)+" times = "+sdt.rounder(charge.value * charge.howManyTimes)+".-     (Sum: "+sdt.rounder(chargeSum)+")</pre></li>"
                    else:
                        chargeSum += charge.value * days
                        text += "<li><pre>"+charge.name+": "+str(charge.value)+".- * "+str(days)+" days = "+sdt.rounder(charge.value * days)+".-     (Sum: "+sdt.rounder(chargeSum)+")</pre></li>"
                text += "</ul>"
        text += "</ul> Sum: "+sdt.rounder(jobSum)+".- in "+sdt.rounder(jobHours)+"h / "+sdt.rounder(jobDays )+" d (+ "+sdt.rounder(chargeSum)+".- charges) <hr />"
        if jobDays != 0:
            loanSplitSumDays = loanSplitSum * (jobDays * (jobHours/jobDays))
        else:
            loanSplitSumDays = 0
        result = jobSum - loanSplitSumDays - creditSum + chargeSum
        #the end of all results..
        text += "<h4>"+tr("Summary")+"</h4>"
        text += "<ul><li><b>"+sdt.rounder(jobSum)+".-</b> </li><li><b> - "+sdt.rounder(loanSplitSumDays)+".-  </b>"+tr("Splits")+"</li><li><b> - "+sdt.rounder(creditSum)+".- </b>"+tr(  "Credits")+"</li> <li><b> + "+sdt.rounder(chargeSum)+".- </b> "+tr("Charges")+"</li></ul><hr /> "+tr("Your company should pay")+"<b> "+sdt.rounder(result)+".- </b>"
        return text
    @staticmethod
    def rounder(nr):
        origNr = nr
        intNr = int(nr)
        afterComma = nr - intNr
        stringComma = str(afterComma)
        if len(stringComma) > 6:
            stringComma = str(abs(float(stringComma)))
            if int(stringComma[4:5]) > 5:
                correctAfterComma = int(stringComma[2:4]) + 1
            else:
                correctAfterComma = int(stringComma[2:4]) 
            floatString = str(intNr)+"."+str(correctAfterComma)
            return floatString
        else:
            return str(origNr)
    @staticmethod
    def createPersonalFinancesHtml(pfList, ui):
        pfHtml = "<ul>"
        pfSum = 0
        for pf in pfList:
            if cw.ifInsertPersonalFinance(ui,  pf):
                pfHtml += "<li>" + pf.name+" @ "+pf.date.toString(dbDateFormat)+": "+pf.plusMinus+str(pf.value)+".-</li>"
                if pf.plusMinus == "+":
                    pfSum += pf.value
                else:
                    pfSum -= pf.value
        pfHtml += "</ul> <h3>Summe: "+str(pfSum)+"</h3>"
        return pfHtml
            
        
        
class maths:
    @staticmethod
    def calcJobSum(company,  job, workCalendar):
        daySpace,  weekendPart = sdt.calcDaySpace(job.startdate, job.enddate, workCalendar,  job.weekendDays)
        hrSpace = daySpace * job.hours
        chargeSum = 0
        for charge in job.wcharges:
            if charge.howManyTimes == 0:
                chargeValue = daySpace * charge.value
            else:
                chargeValue = charge.howManyTimes * charge.value
            chargeSum += chargeValue
        loanSplitSum = 0
        for loanSplit in company.loanSplits:
            if loanSplit.money:
                loanSplitSum += loanSplit.value
            else:
                loanSplitSum += (company.loan / 100) * loanSplit.value
        realHourLoan = (company.loan - loanSplitSum) 
        realHourSplitSum= loanSplitSum * (hrSpace / company.perHours)
        loanSum = realHourLoan * (hrSpace / company.perHours) + chargeSum
        return  (loanSum,  loanSplitSum, realHourLoan, realHourSplitSum,  chargeSum)

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
        print(str(pfCal.month())+"."+str(pfCal.year())+"vs"+str(pf.date.month())+"."+str(pf.date.year()))
        if ui.pfCalendarEnabled.isChecked() == False and ui.pfSearchEnabled.isChecked()==False:
            return True
        elif ui.pfCalendarEnabled.isChecked() and ui.pfSearchEnabled.isChecked()==False:
            if pf.date.month() == pfCal.month() and pf.date.year() == pfCal.year():
                return True
        elif  ui.pfCalendarEnabled.isChecked() == False and  ui.pfSearchEnabled.isChecked():
            pfSearch = ui.pfSearch.text()
            pfSearch = pfSearch.lower()
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
