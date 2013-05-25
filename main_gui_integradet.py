import sqlite3,  os.path,  sys,  re
from main import Ui_MainWindow
from PyQt4 import QtGui, QtCore
dbDateFormat = "dd.MM.yyyy"
fileExist = True
#...dann wird das überprüft..
if os.path.isfile('jobmanagement.db') == False:
    #..und ggf umgestellt..
    fileExist = False
#..denn sqlite3.connect erstellt immer ein file!
db = sqlite3.connect('jobmanagement.db')
#aber wir brauchen ja den cursor, um die db initialisieren zu können.
c = db.cursor()
if fileExist == False:
    c.execute('''CREATE TABLE company (cid  INTEGER PRIMARY KEY, name text, loan real, loankind text, describtion text)''')
    #TODO add weekendDays to job (int) - -1 means no weekend
    c.execute('''CREATE TABLE job (jid  INTEGER PRIMARY KEY, name text, place text, comment text, hours real, correctionHours real, weekendDays INTEGER, startdate text, enddate text, baustellenleiter text, active integer, companyid integer)''')
    c.execute('''CREATE TABLE charges (sid  INTEGER PRIMARY KEY, name text, value real, companyid integer)''')
    c.execute('''CREATE TABLE credit (crid  INTEGER PRIMARY KEY, value real, date text, payed integer, companyid integer)''')
    c.execute('''CREATE TABLE wcharges (wid  INTEGER PRIMARY KEY, jobid INTEGER, chargesid integer)''')
    # if money is false, the measure is in percent..
    c.execute('''CREATE TABLE loanSplits (lsid  INTEGER PRIMARY KEY, name TEXT, value REAL, money INTEGER, companyid INTEGER)''')
    c.execute('''CREATE TABLE loanModel (lmid  INTEGER PRIMARY KEY, name TEXT, perHours REAL)''')
    db.commit()

class Controller:
        def __init__(self):
            self.updateList()
        def createCompany(self, name,  loan,  loankind,  describtion):
            c.execute("INSERT INTO company (name, loan,  loankind, describtion) VALUES (?,?,?,?);",  (name, loan,  loankind, describtion))
            db.commit()
            self.updateList()
        def updateList(self):
            self.companylist = []
            c.execute('select * from company;') 
            for row in c.fetchall():
                self.companylist.append(Company(row[0], row[1], row[2], row[3], row[4]))
        def getCompanyById(self, id):
            for company in self.companylist:
                if company.id == id:
                    return company
                

            
class charges:
    def __init__(self, id,  name,  value):
        self.id = id
        self.name = name
        self.value = value
    def save(self, name, value):
        c.execute("UPDATE charges SET name=?, value=? WHERE sid=?",  (name, float(value), self.id))
        db.commit()
    def delete(self):
        c.execute("DELETE FROM charges WHERE sid=?",  (self.id, ))
        db.commit()
        
class Credit:
    def __init__(self, id,  value,  date, payed,  company):
        self.id = id
        self.value = value
        self.date = date
        if payed == 1:
            self.payed = True
        else: 
            self.payed = False
        self.company = company
    def save(self, value,  date,  payed):
        if payed == True:
            tmpPayed = 1
        else:
            tmpPayed = 0
        c.execute("UPDATE credit SET value=?, date=?, payed=? WHERE crid=?",  (value, date, tmpPayed, str(self.id)))
        db.commit()
    def delete(self):
        c.execute("DELETE FROM credit WHERE crid=?",  (self.id, ))
        db.commit()
        

class Company:
    def __init__(self, id,  name,  loan,  loankind, describtion):
        self.id = id
        self.name = name
        self.loan = loan
        self.loankind =loankind
        self.describtion = describtion
        self.updateJobList()
        self.updatechargesList()
        self.updateCreditList()
    def updateCreditList(self):
        self.credits = []
        c.execute('select * from credit WHERE companyid = ?',  (str(self.id), ))
        for row in c.fetchall():
            self.credits.append(Credit(row[0], row[1], row[2],  row[3],  row[4]))
    def updateJobList(self):
        self.jobs = []
        c.execute('select * from job WHERE companyid = ?',  (str(self.id), ))
        for row in c.fetchall():
            self.jobs.append(Job(row[0], row[1], row[2], row[3], row[4],  row[5],  row[6],  row[7],  row[8],row[9], row[10],  row[11] ))
    def updatechargesList(self):
        self.charges = []
        c.execute('select * from charges WHERE companyid = ?',  (str(self.id), ))
        for row in c.fetchall():
            self.charges.append(charges(row[0], row[1], row[2]))
    def createJob(self,  name, place, comment,  hours, correctionHours,  weekendDays,  startdate,  enddate,  baustellenleiter,  active):
        # (self,  id,  name,  place,  comment,  hours, correctionHours,   startdate,  enddate,  baustellenleiter,  active, companyid):
            c.execute("INSERT INTO job (name, place, comment,hours, correctionHours, weekendDays, startdate, enddate,  baustellenleiter, active, companyid) VALUES (?,?,?,?,?,?,?,?,?,?,?)",  (name, place,  comment, hours,correctionHours,  weekendDays,  startdate, enddate,  baustellenleiter, active,   self.id))
            db.commit()
            self.updateJobList()
    def createSpese(self,  name, value):
            c.execute("INSERT INTO charges (name, value, companyid) VALUES (?,?,?)",  ( name, value,  self.id))
            db.commit()
            self.updatechargesList()
            
    def createCredit(self, value, date, payed):
        if payed == True:
            tmpPayed = 1
        else:
            tmpPayed = 0
            c.execute("INSERT INTO credit (value, date, payed, companyid) VALUES (?,?,?,?)",  ( value, date, tmpPayed, self.id))
            db.commit()
    
    def save(self, name,  loan,  loankind, describtion):
            c.execute("UPDATE company SET name=?, loan=?, loankind=?, describtion=? WHERE cid=?",  (name, loan, loankind, describtion,  self.id))
            db.commit()
    def delete(self):
        c.execute("DELETE FROM company WHERE cid=?",  (self.id, ))
        db.commit()
            

class Job:
    def __init__(self,  id,  name,  place,  comment,  hours, correctionHours, weekendDays,  startdate,  enddate,  baustellenleiter,  active, companyid):
        self.id = id
        self.name = name
        self.place = place
        self.comment = comment
        self.hours = hours
        self.correctionHours = correctionHours
        self.weekendDays = weekendDays
        self.startdate = QtCore.QDate.fromString(startdate, dbDateFormat)
        self.enddate = QtCore.QDate.fromString(enddate, dbDateFormat)
        self.baustellenleiter = baustellenleiter
        self.active = active
        self.companyid = companyid
        self.updateWchargesList()
    def updateWchargesList(self):
        self.wcharges = []
        c.execute('select * from wcharges WHERE jobid = ?',  (str(self.id), ))
        for co in c.fetchall():
            c.execute('select * from charges WHERE sid = ?',  (str(co[2])))
            for row in c.fetchall():
                self.wcharges.append(charges(row[0], row[1], row[2]))
    def addSpese(self,  chargesid):
        c.execute("INSERT INTO wcharges (jobid, chargesid) VALUES (?,?)",  ( self.id, chargesid))
    def removeSpese(self, name,  company):
        for spese in company.charges:
            if spese.name == name:
                c.execute("DELETE FROM wcharges WHERE chargesid=?",  (spese.id, ))
                db.commit()
        
    def save(self, name,  place, comment, hours, correctionHours, weekendDays,  startdate, enddate, baustellenleiter, active, companyid):
            tmpActive = 0
            if active == True:
                tmpActive = 1
            c.execute("UPDATE job SET name=?, place=?, comment=?, hours=?, correctionHours=?, weekendDays=?, startdate=?, enddate=?, baustellenleiter=?, active=?, companyid=? WHERE jid=?",  (name, place,  comment, hours, correctionHours, weekendDays,  startdate, enddate, baustellenleiter, tmpActive, companyid, self.id))
            db.commit()
    def delete(self):
        c.execute("DELETE FROM job WHERE jid=?",  (self.id, ))
        db.commit()
        
mightyController = Controller();
class Gui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        # INIT
        self.showInactive = True
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.updateInfoExel()
        self.ui.loanmodels.addItem("Std")
        self.ui.loanmodels.addItem("3/6/12std")
        cd = QtCore.QDate.currentDate()
        self.ui.startdate.setDate(cd)
        self.ui.enddate.setDate(cd)
        self.ui.creditDate.setDate(cd)
        self.updateCompanyList(True)
        
        #-----------------------
        #Data-Tab
        #-----------------------
        #Item-Clicks
        self.ui.companyList.itemClicked.connect(self.onCompanyItemClick)
        self.ui.jobList.itemClicked.connect(self.onJobItemClick)
        self.ui.creditList.itemClicked.connect(self.onCreditItemClick)
        self.ui.chargesList.itemClicked.connect(self.onSpeseItemClick)
        #Company-Actions
        self.ui.createCompany.clicked.connect(self.onCreateCompany)
        self.ui.saveCompany.clicked.connect(self.onSaveCompany)
        self.ui.deleteCompany.clicked.connect(self.onDeleteCompany)
        #Job-Actions
        self.ui.createJob.clicked.connect(self.onCreateJob)
        self.ui.saveJob.clicked.connect(self.onSaveJob)
        self.ui.deleteJob.clicked.connect(self.onDeleteJob)
        #Spese-Actions
        self.ui.createSpese.clicked.connect(self.onCreateSpese)
        self.ui.saveSpese.clicked.connect(self.onSaveSpese)
        self.ui.deleteSpese.clicked.connect(self.onDeleteSpese)
        self.ui.deleteWorkSpese.clicked.connect(self.onDeleteWorkSpese)
        self.ui.addSpeseToJob.clicked.connect(self.onAddWorkSpese)
        #Credit-Actions
        self.ui.createCredit.clicked.connect(self.onCreateCredit)
        self.ui.saveCredit.clicked.connect(self.onSaveCredit)
        self.ui.deleteCredit.clicked.connect(self.onDeleteCredit)
        
        #--------------------------
        #Showing Tab
        #--------------------------
        #Filter-Actions
        self.ui.showInactive.clicked.connect(self.onShowInactive)
        self.ui.workCalendar.currentPageChanged.connect(self.updateInfoExel)
        self.ui.filterAll.clicked.connect(self.updateInfoExel)
        self.ui.filterCalendar.clicked.connect(self.updateInfoExel)
        self.ui.infoSearch.textChanged.connect(self.updateInfoExel)

        
            #for job in company.jobs:
                #self.ui.jobList.addItem(job.name)
    
    #----------------------
    # Updaters
    #-----------------------
    def updateCompanyList(self, selectFirst=False):
        mightyController.updateList()
        self.ui.companyList.clear()
        for company in mightyController.companylist:
            self.ui.companyList.addItem(company.name)
        if selectFirst:
            self.ui.companyList.setCurrentRow(0)
            self.onCompanyItemClick(self.ui.companyList.currentItem())
    def updateJobList(self, selectFirst=False,  name=""):
        self.ui.jobList.clear()
        self.currentCompany.updateJobList()
        for job in self.currentCompany.jobs:
            if (self.showInactive == True) or (job.active == 1):
                self.ui.jobList.addItem(job.name)
        if selectFirst:
            self.ui.jobList.setCurrentRow(0)
            self.onJobItemClick(self.ui.jobList.currentItem())
    def updatechargesList(self,  selectFirst=False,  name=""):
        self.ui.chargesList.clear()
        self.currentCompany.updatechargesList()
        for spese in self.currentCompany.charges:
            self.ui.chargesList.addItem(spese.name)
        if selectFirst:
            self.ui.chargesList.setCurrentRow(0)
            self.onSpeseItemClick(self.ui.chargesList.currentItem())
    def updateCreditList(self,  selectFirst=False, valueDate=""):
        self.ui.creditList.clear()
        self.currentCompany.updateCreditList()
        for credit in self.currentCompany.credits:
            #if valueDate is not "" and valueDate == str(credit.value) +" "+credit.date:
            self.ui.creditList.addItem(str(credit.value) +" "+credit.date)
        if selectFirst:
            self.ui.creditList.setCurrentRow(0)
            self.onCreditItemClick(self.ui.chargesList.currentItem())
    def updateWorkchargesList(self,  selectFirst=False,  name=""):
        self.ui.workChargesList.clear()
        cs = self.ui.jobList.currentItem()
        for job in self.currentCompany.jobs:
            if cs is not None and job.name == cs.text():
                job.updateWchargesList()
                for wspese in job.wcharges:
                    self.ui.workChargesList.addItem(wspese.name)
        if selectFirst:
            self.ui.workchargesList.setCurrentRow(0)
            
    def onShowInactive(self):
        self.showInactive = self.ui.showInactive.isChecked()
        self.updateJobList(True)
    
    #-------------------------------
    # List-Clicks
    #--------------------------------
    def onCompanyItemClick(self,  item):
        self.ui.jobList.clear()
        self.ui.createJob.setEnabled(True) 
        for company in mightyController.companylist:
            if company.name == item.text():
                self.currentCompany = company
                self.ui.companyname.setText(self.currentCompany.name)
                self.ui.loan.setValue(self.currentCompany.loan)
                self.ui.companydescription.clear()
                self.ui.companydescription.insertPlainText(str(self.currentCompany.describtion))
                self.updateJobList(True)
                self.updatechargesList(True)
                self.updateCreditList(True)
    def onSpeseItemClick(self, item):
        for spese in self.currentCompany.charges:
            if spese.name == item.text():
                self.ui.speseName.setText(spese.name)
                self.ui.speseValue.setValue(spese.value)
    def onCreditItemClick(self, item):
        for credit in self.currentCompany.credits:
            if item is not None and (str(credit.value) +" "+credit.date) == item.text():
                self.ui.creditValue.setValue(credit.value)
                self.ui.creditDate.setDate(QtCore.QDate.fromString(credit.date, dbDateFormat))
    def onJobItemClick(self,  item):
        for job in self.currentCompany.jobs:
            if item is not None and item.text() == job.name:
                self.ui.jobname.setText(job.name)
                self.ui.jobplace.setText(job.place)
                self.ui.jobComment.setPlainText(job.comment)
                self.ui.baustellenleiter.setText(job.baustellenleiter)
                self.ui.hours.cleanText()
                self.ui.hours.setValue(job.hours)
                self.ui.correctionHours.cleanText()
                self.ui.correctionHours.setValue(job.correctionHours)
                self.ui.weekendDays.cleanText()
                self.ui.weekendDays.setValue(job.weekendDays)
                self.ui.startdate.setDate(job.startdate)
                self.ui.enddate.setDate(job.enddate)
                self.ui.daysCalc.setText(str(job.startdate.daysTo(job.enddate)+1)+ " days")
                self.ui.hoursCalc.setText(str((job.startdate.daysTo(job.enddate)+1)*job.hours)+ " hours")
                self.updateWorkchargesList()
                if job.active == 1:
                    self.ui.active.setChecked(True)
                else:
                    self.ui.active.setChecked(False)
    #-------------
    # Charges-Actions
    #--------------
    def onCreateSpese(self):
        self.currentCompany.createSpese(self.ui.speseName.text(), self.ui.speseValue.text())
        # @TODO select the created!
        self.updatechargesList(True)
    def onSaveSpese(self):
        cr = self.ui.chargesList.currentRow()
        cm = self.ui.chargesList.currentItem()
        for spese in self.currentCompany.charges:
            if cm is not None and spese.name == cm.text():
                spese.save(self.ui.chargesName.text(), self.ui.speseValue.text())
                self.ui.status.setText("Charge "+self.ui.chargesName.text()+" saved with success")
        self.updatechargesList()
        self.ui.chargesList.setCurrentRow(cr)
        self.ui.chargesList.setCurrentItem(cm)
    def onDeleteSpese(self):
        cm = self.ui.chargesList.currentItem()
        for spese in self.currentCompany.charges:
            if cm is not None and spese.name == cm.text():
                spese.delete()
                self.ui.status.setText("Charge "+cm.text()+" deleted with success")
        self.updatechargesList(True)
        
    #---------------------------------------
    # Credit-Actions
    #---------------------------------------
    def onCreateCredit(self):
        self.currentCompany.createCredit(self.ui.creditValue.value(), self.ui.creditDate.text(), self.ui.creditPayed.isChecked())
        self.ui.status.setText("credit created?!?"+str(self.ui.creditValue.value()))
        # @TODO select the created!
        self.updateCreditList(selectFirst=True)
    def onSaveCredit(self):
        cr = self.ui.creditList.currentRow()
        cm = self.ui.creditList.currentItem()
        for credit in self.currentCompany.credits:
            if cm is not None and (str(credit.value) +" "+credit.date) == cm.text():
                credit.save(self.ui.creditValue.text(), self.ui.creditDate.text(),   self.ui.creditPayed.isChecked())
                self.ui.status.setText("Credit "+self.ui.creditValue.text()+" saved with success")
        self.updateCreditList()
        self.ui.creditList.setCurrentRow(cr)
    def onDeleteCredit(self):
        cm = self.ui.creditList.currentItem()
        for credit in self.currentCompany.credits:
            if cm is not None and (str(credit.value) +" "+credit.date) == cm.text():
                credit.delete()
                self.ui.status.setText("Credit "+self.ui.creditValue.text()+" deleted with success")
        self.updateCreditList(True)
        
        
    #--------------------
    # Company-Actions
    #---------------------
    def onCreateCompany(self):
        mightyController.createCompany(self.ui.companyname.text(),  self.ui.loan.text(),  self.ui.loanmodels.currentText(),  self.ui.companydescription.toPlainText())
        self.ui.companyList.addItem(self.ui.companyname.text())
    def onSaveCompany(self):
        self.currentCompany.save(self.ui.companyname.text(),  self.ui.loan.text(), self.ui.loanmodels.currentText(), self.ui.companydescription.toPlainText())
        self.updateCompanyList()
    def onDeleteCompany(self):
        self.currentCompany.delete()
        self.updateCompanyList(True)
        
        
    #------------------------
    # Job-Actions
    #------------------------
    def onCreateJob(self):
        tmpCheck = 0
        if self.ui.active.isChecked():
            tmpCheck = 1
        self.currentCompany.createJob(self.ui.jobname.text(), self.ui.jobplace.text(), self.ui.jobComment.toPlainText(), self.ui.hours.text(),self.ui.correctionHours.text(),  self.ui.weekendDays.value(),  self.ui.startdate.text(),  self.ui.enddate.text(),  self.ui.baustellenleiter.text(),  tmpCheck)
        # @TODO select the created!!
        self.ui.jobList.addItem(self.ui.jobname.text())
    def onSaveJob(self):
        cm = self.ui.jobList.currentItem()
        for job in self.currentCompany.jobs:
            if  cm is not None and job.name == str(cm.text()):
                # name,  place,  startdate, enddate, baustellenleiter, active, companyid
                job.save(self.ui.jobname.text(),  self.ui.jobplace.text(),self.ui.jobComment.toPlainText(),   self.ui.hours.text(),self.ui.correctionHours.text(),  self.ui.weekendDays.value(),  self.ui.startdate.text(),  self.ui.enddate.text(),  self.ui.baustellenleiter.text(),  self.ui.active.isChecked(), self.currentCompany.id)
                self.ui.status.setText("Job "+job.name+" saved")
        self.updateJobList()
    def onDeleteJob(self):
        cm = self.ui.jobList.currentItem()
        for job in self.currentCompany.jobs: 
            if  cm is not None and job.name == str(cm.text()):
                job.delete()
        self.updateJobList(True)
    def onDeleteWorkSpese(self):
        cs = self.ui.workchargesList.currentItem()
        cm = self.ui.jobList.currentItem()
        for job in self.currentCompany.jobs: 
            if  cm is not None and job.name == str(cm.text()):
                job.removeSpese(cs.text(),  self.currentCompany)
        self.updateWorkchargesList(True)
    def onAddWorkSpese(self):
        cs = self.ui.chargesList.currentItem()
        cm = self.ui.jobList.currentItem()
        for job in self.currentCompany.jobs:
            if  cm is not None and job.name == cm.text():
                for spese in self.currentCompany.charges:
                    if spese.name == cs.text():
                        job.addSpese(spese.id)
        self.updateWorkchargesList()
        
    #--------------------------
    # Showing-Tab
    #--------------------------
    #ugly method, but how else?
    def updateInfoExel(self):
        self.ui.infoExel.clearContents()
        self.ui.infoExel.clear()
        #proof of concept, have to move..
        self.updateGraphicView()
        rowNr = 0
        self.sum = 0
        self.ui.infoExel.setHorizontalHeaderLabels(("Firmenname", "Jobname",  "Ort",  "Leitung",  "Lohn",  "Zeit (ges.)",  "Tage",  "Min",  "Spesen",  "Summe"))
        wcm = self.ui.workCalendar.monthShown()
        wcy = self.ui.workCalendar.yearShown()
        for company in mightyController.companylist:
            self.ui.infoExel.insertRow(rowNr)
            infoSearch = self.ui.infoSearch.text()
            infoSearch = infoSearch.lower()
            for job in company.jobs:
                daySpace = job.startdate.daysTo(job.enddate) + 1
                if self.ui.filterAll.isChecked():
                    if self.ui.infoSearch.text() != "":
                        jobname = job.name.lower()
                        jobplace = job.place.lower()
                        jobleader = job.baustellenleiter.lower()
                        jobcomment = job.comment.lower()
                        companyname = company.name.lower()                
                    if self.ui.filterCalendar.isChecked():
                        if job.startdate.toString("M") != job.enddate.toString("M"):
                            allDays = job.startdate.daysTo(job.enddate)
                        if job.startdate.toString("M") == str(wcm):
                            daySpace = allDays - job.enddate.day()+1
                        else:
                            daySpace = allDays - (job.startdate.daysInMonth() - job.startdate.day())
                    if self.ui.filterCalendar.isChecked() and self.ui.filterInactive.isChecked() and infoSearch != "":
                        if ((job.startdate.toString("yyyy") == str(wcy)) or (job.enddate.toString("yyyy") == str(wcy))) and (((job.startdate.toString("M") == str(wcm))) or (job.enddate.toString("M") == str(wcm))) and (re.search(infoSearch,  jobname) is not None  or re.search(infoSearch,  jobplace) is not None or re.search(infoSearch,  jobcomment) is not None or re.search(infoSearch,  jobleader) is not None or re.search(infoSearch, companyname) is not None):
                            self.createJobRow(job, company, rowNr, wcm,  daySpace)  
                            rowNr = rowNr + 1
                            self.ui.infoExel.insertRow(rowNr)
                    elif self.ui.filterCalendar.isChecked() == False and self.ui.filterInactive.isChecked() and infoSearch != "":
                        jobname = job.name.lower()
                        jobplace = job.place.lower()
                        jobleader = job.baustellenleiter.lower()
                        jobcomment = job.comment.lower()
                        companyname = company.name.lower()
                        if (re.search(infoSearch,  jobname) is not None  or re.search(infoSearch,  jobplace) is not None or re.search(infoSearch,  jobcomment) is not None or re.search(infoSearch,  jobleader) is not None or re.search(infoSearch,  companyname) is not None):
                            self.createJobRow(job, company, rowNr, wcm,  daySpace)  
                            rowNr = rowNr + 1
                            self.ui.infoExel.insertRow(rowNr)
                    elif self.ui.filterCalendar.isChecked() == False and self.ui.filterInactive.isChecked() and infoSearch == "":
                        self.createJobRow(job, company, rowNr, wcm,  daySpace)  
                        rowNr = rowNr + 1
                        self.ui.infoExel.insertRow(rowNr)
                    elif self.ui.filterCalendar.isChecked() and self.ui.filterInactive.isChecked() and infoSearch == "":
                        if ((job.startdate.toString("yyyy") == str(wcy)) or (job.enddate.toString("yyyy") == str(wcy))) and ((job.startdate.toString("M") == str(wcm))) or (job.enddate.toString("M") == str(wcm)):
                          self.createJobRow(job, company, rowNr, wcm,  daySpace)  
                          rowNr = rowNr + 1
                          self.ui.infoExel.insertRow(rowNr)
                    elif self.ui.filterCalendar.isChecked() and self.ui.filterInactive.isChecked() == False:
                        if ((job.startdate.toString("yyyy") == str(wcy)) or (job.enddate.toString("yyyy") == str(wcy))) and ((job.startdate.toString("M") == str(wcm)) or (job.enddate.toString("M") == str(wcm)) and job.active == 1):
                            self.createJobRow(job, company, rowNr,  wcm,  daySpace)
                            rowNr = rowNr + 1
                            self.ui.infoExel.insertRow(rowNr)
                else:
                    self.createJobRow(job, company,rowNr,  wcm,  daySpace)
                    rowNr = rowNr + 1
                    self.ui.infoExel.insertRow(rowNr)
                    
            self.ui.amount.display(self.sum)
    def createJobRow(self,  job, company, rowNr,  wcm,  daySpace):
        colNr = 0
        minSpace = daySpace * job.hours * 60
        hrSpace = daySpace * job.hours
        spesenSum = 0
        for spese in job.wcharges:
            spesenSum += spese.value
        loanSum = company.loan * hrSpace
        self.sum = self.sum + loanSum + spesenSum
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(company.name) ))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(job.name) ))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(job.place) ))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(job.baustellenleiter) ))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(company.loan * hrSpace) + ".-" ))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(hrSpace) +" Std"))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(daySpace)+ "d (*"+str(job.hours)+"h)"))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(minSpace)+" Min" ))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(spesenSum)+".- " ))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(self.sum)+".-" ))
    def updateGraphicView(self):
        pen= QtGui.QPen(QtCore.Qt.red)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        scene = QtGui.QGraphicsScene()
        scene.addLine(90.70, 90.70, 170.00,  140.00,  pen)
        scene.addLine(170.00,  140.00, 10.00,  20.00,   pen)
        pen.setColor(QtCore.Qt.green)
        pen.setStyle(QtCore.Qt.DotLine)
        scene.addRect(40.00, 40.00, 40.00, 40.00, pen)
        self.ui.graphView.setScene(scene)
        

app = QtGui.QApplication(sys.argv)
jobman = Gui()

jobman.show()

sys.exit(app.exec_())
