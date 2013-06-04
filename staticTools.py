from header import *

def tr(name):
    return QtCore.QCoreApplication.translate("@default",  name)
#semantic designer tools
class sdt:
    @staticmethod
    def calcDaySpace(startdate,  enddate,  cm,  weekendDays):
        if startdate.month() != enddate.month():
            allDays = startdate.daysTo(enddate)
            if startdate.month() == cm:
                daySpace = allDays - enddate.day()+1
            else:
                daySpace = allDays - (startdate.daysInMonth() - startdate.day())
        else:
            daySpace = startdate.daysTo(enddate) + 1
        return daySpace
    @staticmethod
    def createJobRow(ui,  job, company, rowNr,  daySpace, sum):
        colNr = 0
        #minSpace = daySpace * job.hours * 60
        hrSpace = daySpace * job.hours
        spesenSum = 0
        for spese in job.wcharges:
            spesenSum += spese.value
        spesenSum = daySpace * spesenSum
        loanSplitSum = 0
        for loanSplit in company.loanSplits:
            if loanSplit.money:
                loanSplitSum += loanSplit.value
            else:
                loanSplitSum += (company.loan / 100) * loanSplit.value
        realLoan = (company.loan - loanSplitSum) 
        realLoanSplitSum = loanSplitSum * (hrSpace / company.perHours)
        loanSum = realLoan * (hrSpace / company.perHours) + spesenSum
        #building table..
        sumReturn = float(sum) + loanSum
        if not singleView:
            ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(company.name) ))
            colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(job.name) ))
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(job.place) ))
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(job.baustellenleiter) ))
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(sdt.rounder(loanSum) + ".- ("+sdt.rounder(realLoan)+"/std)" ))
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(sdt.rounder(hrSpace) +" Std / "+sdt.rounder(daySpace)+ "d (*"+str(job.hours)+"h)"))
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(sdt.rounder(spesenSum)+".- " ))
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(sdt.rounder(loanSplitSum)+".- ("+sdt.rounder(realLoanSplitSum)+".- @all)" ))
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(sdt.rounder(sumReturn)+".-" ))
        return sumReturn

    @staticmethod
    def updateGraphicView(ui, companyList):
        pen= QtGui.QPen(QtCore.Qt.red)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        scene = QtGui.QGraphicsScene()
        lastLine = 0
        for company in companyList:
            for job in company.jobs:
                scene.addLine(90.70, 90.70, 170.00,  140.00,  pen)
        scene.addLine(170.00,  140.00, 10.00,  20.00,   pen)
        pen.setColor(QtCore.Qt.green)
        pen.setStyle(QtCore.Qt.DotLine)
        scene.addRect(40.00, 40.00, 40.00, 40.00, pen)
        ui.graphView.setScene(scene)
    @staticmethod
    def createDetailText(company, ccm,  ccy, cvCalIsChecked):
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
            text += tr("Loansplitsum")+": "+sdt.rounder(loanSplitSum)+".-/"+str(company.perHours)+tr("h")+"<hr />"
        creditSum = 0
        text += "<h4>"+tr("Credits")+"</h4><ul>"
        for credit in company.credits:
            if (credit.date.month() == ccm and credit.date.year() == ccy) or True is not cvCalIsChecked:
                creditSum += credit.value
                text += "<li>"+credit.date.toString(dbDateFormat) + ": "+str(credit.value)+""
                if credit.payed:
                    text +=".- "+ tr("is")+" "+tr("payed")+"</li>"
                else:
                    text +=".- "+ tr("is NOT")+" "+tr("payed")+"</li>"
        text += "</ul>"
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
                if (job.startdate.month() == ccm and job.startdate.year() == ccy) or (job.enddate.month() == ccm and job.startdate.year() == ccy):
                    days = sdt.calcDaySpace(job.startdate,  job.enddate, ccm,  job.weekendDays)
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
                        text += "<li>"+charge.name+": "+str(charge.value)+".- * "+str(charge.howManyTimes)+" times = "+sdt.rounder(charge.value * days)+".- </li>"
                    else:
                        chargeSum += charge.value * days
                        text += "<li>"+charge.name+": "+str(charge.value)+".- * "+sdt.rounder(days)+"d = "+sdt.rounder(chargeSum)+".- </li>"
                text += "</ul>"
        text += "</ul> Sum: "+sdt.rounder(jobSum)+".- in "+sdt.rounder(jobHours)+"h / "+sdt.rounder(jobDays )+" d (+ "+sdt.rounder(chargeSum)+".- charges) <hr />"
        loanSplitSumDays = loanSplitSum * jobDays
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
    def filterJobs(ui, company, infoSearch, workCalendar, rowNr):
        sum = 0
        ui.infoExel.insertRow(rowNr)
        for job in company.jobs:
            #print(company.name+" "+job.name)
            insertARow = False
            if singleView:
                daySpace = workCalendar.daysInMonth() - (job.weekendDays * 4)
            else:
                daySpace = job.startdate.daysTo(job.enddate) + 1
            if ui.filterAll.isChecked():
                #prepares
                #if ui.infoSearch.text() != "":
                if ui.filterCalendar.isChecked():
                    if singleView:
                        daySpace = dater.daysInMonth() - (job.weekendDays * 4)
                    else:
                        daySpace = sdt.calcDaySpace(job.startdate,  job.enddate, workCalendar.month(),  job.weekendDays)
                if daySpace >= 7:
                    weekendPart = int(daySpace / 7) * job.weekendDays
                    daySpace = daySpace - weekendPart
                #cal + search
                if ui.filterCalendar.isChecked() and ui.filterInactive.isChecked() and infoSearch != "":
                    if cw.checkForValidDate(job.startdate, job.enddate, workCalendar) and  cw.filterTextSearch(infoSearch, job, company):
                        #(ui,  job, company, rowNr,  daySpace, singleView, sum)
                        sum =sdt.createJobRow(ui,  job, company, rowNr,  daySpace, sum) 
                        insertARow = True
                #cal +inactive + search
                if ui.filterCalendar.isChecked() and ui.filterInactive.isChecked() == False and infoSearch != "":
                    if cw.checkForValidDate(job.startdate, job.enddate, workCalendar) and cw.filterTextSearch(infoSearch, job, company) and job.active == 1:
                        sum =sdt.createJobRow(ui,  job, company, rowNr,  daySpace, sum)   
                        insertARow = True
                #search
                elif ui.filterCalendar.isChecked() == False and ui.filterInactive.isChecked() and infoSearch != "":
                    if cw.filterTextSearch(infoSearch, job, company):
                        sum =sdt.createJobRow(ui,  job, company, rowNr,  daySpace, sum) 
                        insertARow = True
                #----- no filters (but filter@all)
                elif ui.filterCalendar.isChecked() == False and ui.filterInactive.isChecked() and infoSearch == "":
                    sum =sdt.createJobRow(ui,  job, company, rowNr,  daySpace, sum) 
                    insertARow = True
                #calendar
                elif ui.filterCalendar.isChecked() and ui.filterInactive.isChecked() and infoSearch == "":
                    if cw.checkForValidDate(job.startdate, job.enddate, workCalendar):
                      sum =sdt.createJobRow(ui,  job, company, rowNr,  daySpace, sum)  
                      insertARow = True
                #inactive calendar
                elif ui.filterCalendar.isChecked() and ui.filterInactive.isChecked() == False and infoSearch == "":
                    if cw.checkForValidDate(job.startdate, job.enddate, workCalendar) and job.active == 1:
                        sum =sdt.createJobRow(ui,  job, company, rowNr,  daySpace, sum)  
                        insertARow = True
                #inactive
                elif ui.filterCalendar.isChecked() ==False and ui.filterInactive.isChecked() == False and infoSearch == "":
                    if  job.active == 1:
                        sum =sdt.createJobRow(ui,  job, company, rowNr,  daySpace, sum)  
                        insertARow = True
                #inactive + search
                elif ui.filterCalendar.isChecked() ==False and ui.filterInactive.isChecked() == False and infoSearch != "":
                    if  cw.filterTextSearch(infoSearch, job, company) and job.active == 1:
                        sum=sdt.createJobRow(ui,  job, company, rowNr,  daySpace, sum)  
                        insertARow = True
            else:
                sum=sdt.createJobRow(ui,  job, company, rowNr,  daySpace, sum) 
                insertARow = True
            if insertARow:
                print(company.name + " RowNr:"+str(rowNr)+ " [R:"+str(workCalendar.month())+"]")
                rowNr += 1
                ui.infoExel.insertRow(rowNr)
        return (rowNr, sum)
class cw:
    @staticmethod
    def checkForValidDate(startdate, enddate,  wCalendarDate):
        return (startdate.month() == wCalendarDate.month() and startdate.year() == wCalendarDate.year()) or (enddate.month() == wCalendarDate.month() and startdate.year() == wCalendarDate.year())
    def filterTextSearch(infoSearch,  job,  company):
        return (re.search(infoSearch,  job.name.lower()) is not None  or re.search(infoSearch,  job.place.lower()) is not None or re.search(infoSearch,  job.comment.lower()) is not None or re.search(infoSearch,  job.baustellenleiter.lower()) is not None or re.search(infoSearch, company.name.lower()) is not None)
