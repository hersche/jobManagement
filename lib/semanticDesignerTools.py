from lib.staticTools import *
#semantic designer tools
class sdt:
    @staticmethod
    def aB(text):
        alertBox = QtGui.QMessageBox()
        alertBox.setText(text)
        alertBox.exec__()
    @staticmethod
    def calcDaySpace(startdate,  enddate,  wc,  weekendDays, noCalendar = False):
        if startdate.daysTo(enddate) == 0:
            daySpace = 1
        elif startdate.month() != enddate.month() and noCalendar==False:
            allDays = startdate.daysTo(enddate)
            if startdate.month() == wc.month():
                daySpace = allDays - enddate.day()+1
            else:
                daySpace = allDays - (startdate.daysInMonth() - startdate.day())
        elif noCalendar:
                daySpace = startdate.daysTo(enddate) + 1
        else:
            daySpace = startdate.daysTo(enddate) + 1
        weekendPart = int(daySpace / 7) * weekendDays
        daySpace = daySpace - weekendPart
        return (daySpace,  weekendPart)
    @staticmethod
    def createJobRow(ui,  job, company, workCalendar,  rowNr, sum):
        colNr = 0
        if not singleView:
            if ui.filterAll.isChecked() and ui.filterCalendar .isChecked():
                daySpace,  weekendPart = sdt.calcDaySpace(job.startdate,  job.enddate, workCalendar,  job.weekendDays)
            else:
                daySpace,  weekendPart = sdt.calcDaySpace(job.startdate,  job.enddate, workCalendar,  job.weekendDays, noCalendar=True)
            
        else:
            daySpace,  weekendPart = (workCalendar.daysInMonth() - (job.weekendDays * 4), job.weekendDays)
        #minSpace = daySpace * job.hours * 60
        loanSum,  loanDistractionSum, realHourLoan, realHourSplitSum,  chargeSum = maths.calcJobSum(company,  job,  workCalendar)
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
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(maths.rounder(loanSum) + ".- ("+maths.rounder(realHourLoan)+"/std)" ))
        colNr = colNr + 1
        w = QtGui.QTableWidgetItem(maths.rounder((daySpace * job.hours)+job.correctionHours) +" Std")
        w.setToolTip(tr("From")+" "+job.startdate.toString(dbDateFormat)+" to "+job.enddate.toString(dbDateFormat)+ "<hr />"+maths.rounder(daySpace)+ "d (*"+str(job.hours)+"h)+"+str(job.correctionHours)+"correctionH. "+str(weekendPart)+"d was Weekenddays")
        ui.infoExel.setItem(rowNr,  colNr,   w)
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(maths.rounder(chargeSum)+".- " ))
        colNr = colNr + 1
        w = QtGui.QTableWidgetItem(maths.rounder(realHourSplitSum)+".- @all")
        w.setToolTip(maths.rounder(loanDistractionSum)+".-/"+str(company.perHours)+tr("h")+")")
        ui.infoExel.setItem(rowNr,  colNr,   w)
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(maths.rounder(sum + loanSum)+".-" ))
        return loanSum
    @staticmethod
    def colorChanger(color):
        if color > 200:
            return 25
        else:
            return color + 53
    @staticmethod
    def updateGraphicView(ui, companyList, workCalendar, infoSearch):
        pen=QtGui.QPen(QtCore.Qt.red)
        r, g, b=(120, 77, 99)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setWidth(4)
        if ui.filterAll.isChecked() and ui.filterCalendar.isChecked():
            widthPerHour = 2.8
        else:
            widthPerHour = 2.0
        scene = QtGui.QGraphicsScene()
        pen.setColor(QtGui.QColor(188, 188, 188))
        scene.addLine(0,0,450,0,pen)
        pen=QtGui.QPen(QtCore.Qt.yellow)
        r, g, b=(120, 77, 99)
        pen.setColor(QtGui.QColor(r, g, b))
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setWidth(1)
        #lastLine = 0
        oldDaySpace = 0.00
        oldValue = 0.00
        allValue = 0
#         qtPainter = QtGui.QPainter()
#         brush = QtGui.QBrush()
#         brush.setColor(QtGui.QColor(120,120,250))
#         qtPainter.setBackground()
        for company in companyList:
            for job in company.jobs:
                if cw.insertJobYesNo(ui, company, job, infoSearch, workCalendar):
                    daySpace,  weekendPart = sdt.calcDaySpace(job.startdate, job.enddate, workCalendar,  job.weekendDays)
                    loanSum,  loanDistractionSum, realHourLoan,  realHourSplitSum,  chargeSum = maths.calcJobSum(company,  job,  workCalendar)
                    daySpace = ((daySpace * job.hours) + job.correctionHours )
                    daySpace = (daySpace + oldDaySpace) / 2
                    value = ((company.loan/10)*daySpace)
                    allValue += value
                    scene.addLine(float(oldDaySpace),0,float(daySpace*widthPerHour)/2,float(-loanSum/40),pen)
                    scene.addLine(float(daySpace*widthPerHour)/2,float(-loanSum/40),float(daySpace*widthPerHour),0,pen)
                    # old - scene.addLine(float(oldDaySpace),float(-oldValue),float(daySpace*widthPerHour),float(-loanSum/50),pen)
                    oldDaySpace = daySpace*widthPerHour
                    #oldValue = loanSum/50
                    r=sdt.colorChanger(r)
                    g=sdt.colorChanger(g)
                    b=sdt.colorChanger(b)
                    pen.setColor(QtGui.QColor(r, g, b))
        ui.graphView.setScene(scene)
        
    @staticmethod 
    def createCreditTextBox(company, ui):
        wc = QtCore.QDate.fromString(str(ui.workCalendar.monthShown())+"."+str(ui.workCalendar.yearShown()),"M.yyyy")
        creditString =""
        fCreditString = ""
        creditSum = 0
        #change to check credit-list-size
        for credit in company.credits:
            if (ui.filterCalendar.isChecked() and credit.date.month() == wc.month() and credit.date.year() == wc.year()) or ui.filterCalendar.isChecked() == False:
                creditSum += credit.value
                creditString += "<li><pre>"+credit.name+" @"+credit.date.toString(dbDateFormat)+":      "+str(credit.value)+"</pre><li/>"
        if len(company.credits) > 0 and creditSum > 0:
            fCreditString = "<ul>"
            creditString += "</ul>"+company.name+": "+str(creditSum)+"<br />"
            fCreditString += creditString
        return (fCreditString,  creditSum)
    @staticmethod
    def createDetailText(company, workCalendar, cvCalIsChecked):
        text = ""
        text += "<h1>"+company.name+"</h1>"+company.describtion+"<br />"+tr("Loan")+": "+str(company.loan)+" (per "+str(company.perHours)+tr("h")+")<hr />"
        loanDistractionSum = 0
        #LoanSplits
        text += "<h4>"+tr("loanDistractions")+"</h4><ul>"
        for ls in  company.loanDistractions:
            text += "<li>"+ls.name+": "+str(ls.value)
            if ls.money:
                loanDistractionSum += ls.value
                text += ".- </li>"
            else:
                inMoney = (company.loan / 100) * ls.value
                loanDistractionSum += inMoney
                text += "% ("+maths.rounder(inMoney)+".-) </li>"
        text += "</ul>"
        if loanDistractionSum > 0:
            text += tr("Loandistractionsum")+": "+maths.rounder(loanDistractionSum)+".-/"+str(company.perHours)+" "+tr("h")+"<hr />"
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
            text += tr("Creditsum")+": "+maths.rounder(creditSum)+".- <hr />"
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
                text += "<li>"+job.name+": "+maths.rounder(days)+"d * ("+maths.rounder(job.hours)+"h /"+str(company.perHours)+" )+" +str(job.correctionHours)+"h = "+maths.rounder(hourSpace)+"h * " + str(company.loan)+".-  ="+maths.rounder(hourSpace*company.loan)+".- </li>"
                text += "<ul>"
                for charge in job.wcharges:
                    if charge.howManyTimes > 0:
                        chargeSum += charge.value * charge.howManyTimes
                        text += "<li><pre>"+charge.name+": "+str(charge.value)+".- * "+str(charge.howManyTimes)+" times = "+maths.rounder(charge.value * charge.howManyTimes)+".-     (Sum: "+maths.rounder(chargeSum)+")</pre></li>"
                    else:
                        chargeSum += charge.value * days
                        text += "<li><pre>"+charge.name+": "+str(charge.value)+".- * "+str(days)+" days = "+maths.rounder(charge.value * days)+".-     (Sum: "+maths.rounder(chargeSum)+")</pre></li>"
                text += "</ul>"
        text += "</ul> Sum: "+maths.rounder(jobSum)+".- in "+maths.rounder(jobHours)+"h / "+maths.rounder(jobDays )+" d (+ "+maths.rounder(chargeSum)+".- charges) <hr />"
        if jobDays != 0:
            loanDistractionSumDays = loanDistractionSum * (jobDays * (jobHours/jobDays))
        else:
            loanDistractionSumDays = 0
        result = jobSum - loanDistractionSumDays - creditSum + chargeSum
        #the end of all results..
        text += "<h4>"+tr("Summary")+"</h4>"
        text += "<ul><li><b>"+maths.rounder(jobSum)+".-</b> </li><li><b> - "+maths.rounder(loanDistractionSumDays)+".-  </b>"+tr("Splits")+"</li><li><b> - "+maths.rounder(creditSum)+".- </b>"+tr(  "Credits")+"</li> <li><b> + "+maths.rounder(chargeSum)+".- </b> "+tr("Charges")+"</li></ul><hr /> "+tr("Your company should pay")+"<b> "+maths.rounder(result)+".- </b>"
        return text

    @staticmethod
    def createPersonalFinancesHtml(pfList, ui):
        pfHtml = "<ul>"
        pfSum = 0
        timeRepeat = 0
        calChecked = ui.pfCalendarEnabled.isChecked()
        for pf in pfList:
            if cw.ifInsertPersonalFinance(ui,pf):
                if pf.repeat != "None":
                    if pf.repeat=="Daily":
                        if calChecked:
                            timeRepeat = pf.date.daysInMonth() - pf.date.day()
                            if not pf.timesRepeat > timeRepeat:
                                 timeRepeat = pf.timesRepeat
                        else:
                            timeRepeat = pf.timesRepeat

                    elif pf.repeat=="Weekly":
                        if calChecked:
                            timeRepeat = pf.date.daysInMonth() - pf.date.day()
                            timeRepeat = timeRepeat / 7
                            if not pf.timesRepeat > timeRepeat:
                                 timeRepeat = pf.timesRepeat

                    
                pfHtml += "<li>" + pf.name+" @ "+pf.date.toString(dbDateFormat)+": "+pf.plusMinus+str(pf.value)+".- in "+str(timeRepeat)+" times = "+str(pf.value*timeRepeat)+"</li>"
                if pf.plusMinus == "+":
                    pfSum += pf.value
                else:
                    pfSum -= pf.value
        pfHtml += "</ul> <h3>Summe: "+str(pfSum)+"</h3>"
        return pfHtml
            
      