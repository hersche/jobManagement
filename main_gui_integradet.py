#this code is GPL-FORCED so let changes open, pls!!
#License @ http://www.gnu.org/licenses/gpl.txt
#Author: skamster

import sqlite3,  os.path,  sys,  re
from main import Ui_MainWindow
from PyQt4 import QtGui, QtCore
dbDateFormat = "dd.MM.yyyy"
fileExist = True
def tr(name, bla=""):
    return QtCore.QCoreApplication.translate("@default",  name)
#...dann wird das überprüft..
if os.path.isfile('jobmanagement.db') == False:
    #..und ggf umgestellt..
    fileExist = False
#..denn sqlite3.connect erstellt immer ein file!
db = sqlite3.connect('jobmanagement.db')
#aber wir brauchen ja den cursor, um die db initialisieren zu können.
c = db.cursor()
if fileExist == False:
    c.execute("CREATE TABLE company (cid  INTEGER PRIMARY KEY, name text, loan REAL, perHours REAL, describtion text)")
    #TODO add weekendDays to job (int) - -1 means no weekend
    c.execute("CREATE TABLE job (jid  INTEGER PRIMARY KEY, name text, place text, comment text, hours real, correctionHours real, weekendDays INTEGER, startdate text, enddate text, baustellenleiter text, active integer, companyid integer)")
    c.execute("CREATE TABLE charges (sid  INTEGER PRIMARY KEY, name text, value real, companyid integer)")
    c.execute("CREATE TABLE credit (crid  INTEGER PRIMARY KEY, value real, date text, payed integer, companyid integer)")
    c.execute("CREATE TABLE wcharges (wid  INTEGER PRIMARY KEY, jobid INTEGER, chargesid integer)")
    # if money is false, the measure is in percent..
    c.execute("CREATE TABLE loanSplit (lsid  INTEGER PRIMARY KEY, name TEXT, value REAL, money INTEGER, companyid INTEGER)")
    c.execute("CREATE TABLE config (coid INTEGER PRIMARY KEY,  key TEXT,  value TEXT)")
    
    db.commit()
    

class Controller:
        def __init__(self):
            self.updateList()
            self.updateConfigList()
        def createCompany(self, name,  loan,  perHours,  describtion):
            c.execute("INSERT INTO company (name, loan,  perHours, describtion) VALUES (?,?,?,?);",  (name, loan,  perHours, describtion))
            db.commit()
            self.updateList()
        def updateList(self):
            self.companylist = []
            c.execute('select * from company;') 
            for row in c.fetchall():
                self.companylist.append(Company(row[0], row[1], row[2], row[3], row[4]))
        def createConfig(self, key,  value):
            c.execute("INSERT INTO config (key, value) VALUES (?,?);",  (key, value))
            db.commit()
            self.updateConfigList()
        def updateConfigList(self):
            self.configlist = []
            c.execute('select * from config;') 
            for row in c.fetchall():
                self.configlist.append(Config(row[0], row[1], row[2]))
        def getCompanyById(self, id):
            for company in self.companylist:
                if company.id == id:
                    return company
                    
class Config:
    #"CREATE TABLE config (coid INTEGER PRIMARY KEY,  key TEXT,  value TEXT)
    def __init__(self,  id,  key,  value):
        self.id = id
        self.key = key
        self.value = value
        
    def save(self, key,  value):
        c.execute("UPDATE config SET key=?, value=? WHERE coid=?",  (key, value,  self.id))
        db.commit()
    def delete(self):
        c.execute("DELETE FROM config WHERE coid=?",  (self.id, ))
        db.commit()
        
                
class loanSplit:
    #CREATE TABLE loanSplit (lsid  INTEGER PRIMARY KEY, name TEXT, value REAL, money INTEGER, companyid INTEGER)"
    def __init__(self, id,  name, value,  money):
        self.id = id
        self.name = name
        self.value = value
        if money == 1:
            #The value is calcucalted as money (.-)
            self.money = True
        else:
            #The value is calculated as percent (%)
            self.money = False
    def save(self, name,  value,  money):
        tmpMoney = 0
        if money==True:
            tmpMoney = 1
        c.execute("UPDATE loanSplit SET name=?, value=?, money=? WHERE lsid=?",  (name, float(value), tmpMoney,  self.id))
        db.commit()
    def delete(self):
        c.execute("DELETE FROM loanSplit WHERE lsid=?",  (self.id, ))
        db.commit()
    
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
        self.date = QtCore.QDate.fromString(date, dbDateFormat)
        if payed == 1:
            self.payed = True
        else: 
            self.payed = False
        self.company = company
    def save(self, value,  date,  payed):
        tmpPayed = 0
        if payed == True:
            tmpPayed = 1
        c.execute("UPDATE credit SET value=?, date=?, payed=? WHERE crid=?",  (value, date, tmpPayed, str(self.id)))
        db.commit()
    def delete(self):
        c.execute("DELETE FROM credit WHERE crid=?",  (self.id, ))
        db.commit()
        

class Company:
    def __init__(self, id,  name,  loan, perHours,  describtion):
        self.id = id
        self.name = name
        self.loan = loan
        self.perHours = perHours
        self.describtion = describtion
        self.updateJobList()
        self.updatechargesList()
        self.updateCreditList()
        self.updateLoanSplitList()
        

    def updateLoanSplitList(self):
        self.loanSplits = []
        c.execute("SELECT * FROM loanSplit WHERE companyid = ?", (str(self.id), ))
        for row in c.fetchall():
            self.loanSplits.append(loanSplit(row[0], row[1],row[2],row[3]))
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
            
    def createLoanSplit(self, name, value, money):
        if money == True:
            tmpMoney = 1
        else:
            tmpMoney = 0
        c.execute("INSERT INTO loanSplit (name, value, money, companyid) VALUES (?,?,?,?)",  ( name, value, tmpMoney,  self.id))
        db.commit()
        
    def createCredit(self, value, date, payed):
        if payed:
            tmpPayed = 1
        else:
            tmpPayed = 0
        c.execute("INSERT INTO credit (value, date, payed, companyid) VALUES (?,?,?,?)",  ( value, date, tmpPayed, self.id))
        db.commit()
    
    def save(self, name,  loan,  perHours, describtion):
            c.execute("UPDATE company SET name=?, loan=?, perHours=?, describtion=? WHERE cid=?",  (name, loan, perHours, describtion,  self.id))
            db.commit()
    def delete(self):
        c.execute("DELETE FROM job WHERE companyid=?",  (self.id, ))
        c.execute("DELETE FROM charges WHERE companyid=?",  (self.id, ))
        c.execute("DELETE FROM loanSplit WHERE companyid=?",  (self.id, ))
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
        c.execute("DELETE FROM wcharges WHERE jobid=?",  (self.id, ))
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
        cd = QtCore.QDate.currentDate()
        self.ui.startdate.setDate(cd)
        self.ui.enddate.setDate(cd)
        self.ui.creditDate.setDate(cd)
        self.updateCompanyList(True)
        self.updateInfoExel()
        self.updateCompanyView()
        self.updateConfigList()
        
        #-----------------------
        #Data-Tab
        #-----------------------
        #Item-Clicks
        self.ui.companyList.itemClicked.connect(self.onCompanyItemClick)
        self.ui.jobList.itemClicked.connect(self.onJobItemClick)
        self.ui.creditList.itemClicked.connect(self.onCreditItemClick)
        self.ui.chargesList.itemClicked.connect(self.onSpeseItemClick)
        self.ui.loanSplitList.itemClicked.connect(self.onLoanSplitItemClick)
        self.ui.configList.itemClicked.connect(self.onConfigItemClick)
        #Company-Actions
        self.ui.createCompany.clicked.connect(self.onCreateCompany)
        self.ui.saveCompany.clicked.connect(self.onSaveCompany)
        self.ui.deleteCompany.clicked.connect(self.onDeleteCompany)
        #Job-Actions
        self.ui.createJob.clicked.connect(self.onCreateJob)
        self.ui.saveJob.clicked.connect(self.onSaveJob)
        self.ui.deleteJob.clicked.connect(self.onDeleteJob)
        #Spese-Actions
        self.ui.createCharge.clicked.connect(self.onCreateSpese)
        self.ui.saveCharge.clicked.connect(self.onSaveSpese)
        self.ui.deleteCharge.clicked.connect(self.onDeleteSpese)
        self.ui.deleteWorkSpese.clicked.connect(self.onDeleteWorkSpese)
        self.ui.addChargeToJob.clicked.connect(self.onAddWorkSpese)
        #Credit-Actions
        self.ui.createCredit.clicked.connect(self.onCreateCredit)
        self.ui.saveCredit.clicked.connect(self.onSaveCredit)
        self.ui.deleteCredit.clicked.connect(self.onDeleteCredit)
        
        #loanSplit-Actions
        self.ui.createLoanSplit.clicked.connect(self.onCreateLoanSplit)
        self.ui.saveLoanSplit.clicked.connect(self.onSaveLoanSplit)
        self.ui.deleteLoanSplit.clicked.connect(self.onDeleteLoanSplit)
        
        #config-Actions
        self.ui.createConfig.clicked.connect(self.onCreateConfig)
        self.ui.saveConfig.clicked.connect(self.onSaveConfig)
        self.ui.deleteConfig.clicked.connect(self.onDeleteConfig)
        
        #--------------------------
        #Showing Tab
        #--------------------------
        #Filter-Actions
        self.ui.showInactive.clicked.connect(self.onShowInactive)
        self.ui.workCalendar.currentPageChanged.connect(self.updateInfoExel)
        self.ui.filterAll.clicked.connect(self.updateInfoExel)
        self.ui.filterCalendar.clicked.connect(self.updateInfoExel)
        self.ui.filterInactive.clicked.connect(self.updateInfoExel)
        self.ui.infoSearch.textChanged.connect(self.updateInfoExel)
        #--------------------------
        # CompanyView
        #---------------------------
        self.ui.companyViewList.currentIndexChanged.connect(self.updateCompanyView)
        self.ui.companyViewCalendar.currentPageChanged.connect(self.updateCompanyView)
        self.ui.companyViewCalendarFilter.clicked.connect(self.updateCompanyView)
    
    
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
            
    def updateLoanSplitList(self,  selectFirst=False,  name=""):
        self.ui.loanSplitList.clear()
        self.currentCompany.updateLoanSplitList()
        for loanSplit in self.currentCompany.loanSplits:
            self.ui.loanSplitList.addItem(loanSplit.name)
        if selectFirst:
            self.ui.loanSplitList.setCurrentRow(0)
            self.onLoanSplitItemClick(self.ui.loanSplitList.currentItem())
    def updateConfigList(self,  selectFirst=False,  name=""):
        self.ui.configList.clear()
        mightyController.updateConfigList()
        for config in mightyController.configlist:
            self.ui.configList.addItem(config.key)
        if selectFirst:
            self.ui.configList.setCurrentRow(0)
            self.onConfigItemClick(self.ui.configList.currentItem())
            
    def updateCreditList(self,  selectFirst=False, valueDate=""):
        self.ui.creditList.clear()
        self.currentCompany.updateCreditList()
        for credit in self.currentCompany.credits:
            #if valueDate is not "" and valueDate == str(credit.value) +" "+credit.date:
            self.ui.creditList.addItem(str(credit.value) +" "+credit.date.toString(dbDateFormat))
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
            self.ui.workChargesList.setCurrentRow(0)
            
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
                self.ui.perHours.setValue(self.currentCompany.perHours)
                self.ui.companydescription.clear()
                self.ui.companydescription.insertPlainText(str(self.currentCompany.describtion))
                self.updateJobList(True)
                self.updatechargesList(True)
                self.updateCreditList(True)
                self.updateLoanSplitList(True)
    def onSpeseItemClick(self, item):
        for spese in self.currentCompany.charges:
            if spese.name == item.text():
                self.ui.chargesName.setText(spese.name)
                self.ui.chargesValue.setValue(spese.value)
    def onLoanSplitItemClick(self, item):
        for loanSplit in self.currentCompany.loanSplits:
            if loanSplit.name == item.text():
                self.ui.loanSplitName.setText(loanSplit.name)
                self.ui.loanSplitValue.setValue(loanSplit.value)
                self.ui.loanSplitMoney.setChecked(loanSplit.money)
    def onConfigItemClick(self, item):
        for config in mightyController.configlist:
            if config.key == item.text():
                self.ui.configKey.setText(config.key)
                self.ui.configValue.setText(config.value)
    def onCreditItemClick(self, item):
        for credit in self.currentCompany.credits:
            if item is not None and (str(credit.value) +" "+credit.date.toString(dbDateFormat)) == item.text():
                self.ui.creditValue.setValue(credit.value)
                self.ui.creditDate.setDate(credit.date)
                if credit.payed:
                    self.ui.creditPayed.setChecked(True)
                else:
                    self.ui.creditPayed.setChecked(False)
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
                self.ui.daysCalc.setText(str(job.startdate.daysTo(job.enddate)+1)+  tr("days"))
                self.ui.hoursCalc.setText(str((job.startdate.daysTo(job.enddate)+1)*job.hours)+ tr(" hours"))
                self.updateWorkchargesList()
                if job.active == 1:
                    self.ui.active.setChecked(True)
                else:
                    self.ui.active.setChecked(False)
    #-------------
    # Charges-Actions
    #--------------
    def onCreateSpese(self):
        self.currentCompany.createSpese(self.ui.chargesName.text(), self.ui.chargesValue.text())
        # @TODO select the created!
        self.updatechargesList(True)
    def onSaveSpese(self):
        cr = self.ui.chargesList.currentRow()
        cm = self.ui.chargesList.currentItem()
        for spese in self.currentCompany.charges:
            if cm is not None and spese.name == cm.text():
                spese.save(self.ui.chargesName.text(), self.ui.chargesValue.text())
                self.ui.status.setText("Charge "+self.ui.chargesName.text()+tr("saved"))
        self.updatechargesList(True)
        
        self.updateWorkchargesList(True)
        self.ui.chargesList.setCurrentRow(cr)
        self.ui.chargesList.setCurrentItem(cm)
    def onDeleteSpese(self):
        cm = self.ui.chargesList.currentItem()
        for spese in self.currentCompany.charges:
            if cm is not None and spese.name == cm.text():
                spese.delete()
                self.ui.status.setText("Charge "+cm.text()+tr("deleted"))
        self.updatechargesList(True)
    #-------------
    # loanSplit-Actions
    #--------------
    def onCreateLoanSplit(self):
        self.currentCompany.createLoanSplit(self.ui.loanSplitName.text(), self.ui.loanSplitValue.text(),  self.ui.loanSplitMoney.isChecked())
        # @TODO select the created!
        self.ui.status.setText("LoanSplit "+self.ui.loanSplitName.text()+tr("created"))
        self.updateLoanSplitList(True)
    def onSaveLoanSplit(self):
        cr = self.ui.loanSplitList.currentRow()
        cm = self.ui.loanSplitList.currentItem()
        for loanSplit in self.currentCompany.loanSplits:
            if cm is not None and loanSplit.name == cm.text():
                loanSplit.save(self.ui.loanSplitName.text(), self.ui.loanSplitValue.text(),  self.ui.loanSplitMoney.isChecked())
                self.ui.status.setText("LoanSplit "+self.ui.loanSplitName.text()+tr("saved"))
        self.updateLoanSplitList()
        self.ui.loanSplitList.setCurrentRow(cr)
        self.ui.loanSplitList.setCurrentItem(cm)
    def onDeleteLoanSplit(self):
        cm = self.ui.loanSplitList.currentItem()
        for loanSplit in self.currentCompany.loanSplits:
            if cm is not None and loanSplit.name == cm.text():
                loanSplit.delete()
                self.ui.status.setText("Charge "+cm.text()+tr("deleted"))
        self.updateLoanSplitList(True)
        
    #-------------
    # config-Actions
    #--------------
    def onCreateConfig(self):
        mightyController.createConfig(self.ui.configKey.text(), self.ui.configValue.text())
        # @TODO select the created!
        self.ui.status.setText(tr("Config")+" "+self.ui.configKey.text()+" "+tr("created"))
        self.updateConfigList(True)
    def onSaveConfig(self):
        cr = self.ui.configList.currentRow()
        cm = self.ui.configList.currentItem()
        for config in mightyController.configlist:
            if cm is not None and config.key == cm.text():
                config.save(self.ui.configKey.text(), self.ui.configValue.text())
                self.ui.status.setText("LoanSplit "+self.ui.configKey.text()+" "+tr("saved"))
        self.updateConfigList()
        self.ui.configList.setCurrentRow(cr)
        self.ui.configList.setCurrentItem(cm)
    def onDeleteConfig(self):
        cm = self.ui.configList.currentItem()
        for config in mightyController.configlist:
            if cm is not None and config.key == cm.text():
                config.delete()
                self.ui.status.setText("Charge "+cm.text()+" "+tr("deleted"))
        self.updateConfigList(True)
        
    #---------------------------------------
    # Credit-Actions
    #---------------------------------------
    def onCreateCredit(self):
        self.currentCompany.createCredit(self.ui.creditValue.value(), self.ui.creditDate.text(), self.ui.creditPayed.isChecked())
        self.ui.status.setText("credit"+tr("created")+":"+str(self.ui.creditValue.value()))
        # @TODO select the created!
        self.updateCreditList(selectFirst=True)
    def onSaveCredit(self):
        cr = self.ui.creditList.currentRow()
        cm = self.ui.creditList.currentItem()
        for credit in self.currentCompany.credits:
            if cm is not None and (str(credit.value) +" "+credit.date.toString(dbDateFormat)) == cm.text():
                credit.save(self.ui.creditValue.text(), self.ui.creditDate.text(),   self.ui.creditPayed.isChecked())
                self.ui.status.setText("Credit "+self.ui.creditValue.text()+" saved")
        self.updateCreditList()
        self.ui.creditList.setCurrentRow(cr)
    def onDeleteCredit(self):
        cm = self.ui.creditList.currentItem()
        for credit in self.currentCompany.credits:
            if cm is not None and (str(credit.value) +" "+credit.date.toString(dbDateFormat)) == cm.text():
                credit.delete()
                self.ui.status.setText("Credit "+self.ui.creditValue.text()+" deleted")
        self.updateCreditList(True)
        
        
    #--------------------
    # Company-Actions
    #---------------------
    def onCreateCompany(self):
        mightyController.createCompany(self.ui.companyname.text(),  self.ui.loan.text(),  self.ui.perHours.text(),  self.ui.companydescription.toPlainText())
        self.ui.companyList.addItem(self.ui.companyname.text())
    def onSaveCompany(self):
        self.currentCompany.save(self.ui.companyname.text(),  self.ui.loan.text(), self.ui.perHours.text(), self.ui.companydescription.toPlainText())
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
        cs = self.ui.workChargesList.currentItem()
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
                    if cs is not None and spese.name == cs.text():
                        job.addSpese(spese.id)
                        job.updateWchargesList()
        self.updateWorkchargesList()
    def rounder(self, nr):
        origNr = nr
        intNr = int(nr)
        afterComma = nr - intNr
        stringComma = str(afterComma)
        if len(stringComma) > 5:
            if int(stringComma[4:5]) > 5:
                correctAfterComma = int(stringComma[2:4]) + 1
            else:
                correctAfterComma = int(stringComma[2:4])
            floatString = str(intNr)+"."+str(correctAfterComma)
            return floatString
        else:
            return str(origNr)
    def calcDaySpace(self,  startdate,  enddate,  cm,  weekendDays):
        if startdate.toString("M") != enddate.toString("M"):
            allDays = startdate.daysTo(enddate)
            if startdate.toString("M") == str(cm):
                daySpace = allDays - enddate.day()+1
            else:
                daySpace = allDays - (startdate.daysInMonth() - startdate.day())
        else:
            daySpace = startdate.daysTo(enddate) + 1
        if daySpace > 7:
            weekendPart = (daySpace / 7) * weekendDays
            daySpace = daySpace - weekendPart
        return daySpace
    #--------------------------
    # Showing-Tab
    #--------------------------
    #ugly method, but how else?
    def updateInfoExel(self):
        self.ui.infoExel.clearContents()
        self.ui.infoExel.clear()
        #proof of concept, have to move..
        self.updateGraphicView()
        self.updateCompanyViewList()
        rowNr = 0
        self.sum = 0
        self.ui.infoExel.setHorizontalHeaderLabels((tr( "Companyname"),tr( "Jobname"),tr( "Place"), tr( "Leader"), tr( "Loan"),tr( "Time"), tr(  "Spesen", ""), tr( "Splits", ""), tr( "Summe", "")))
        wcm = self.ui.workCalendar.monthShown()
        wcy = self.ui.workCalendar.yearShown()
        creditString =""
        for company in mightyController.companylist:
            self.ui.infoExel.insertRow(rowNr)
            infoSearch = self.ui.infoSearch.text()
            infoSearch = infoSearch.lower()
            for job in company.jobs:
                insertARow = False
                daySpace = job.startdate.daysTo(job.enddate) + 1
                if self.ui.filterAll.isChecked():
                    
                    if self.ui.infoSearch.text() != "":
                        jobname = job.name.lower()
                        jobplace = job.place.lower()
                        jobleader = job.baustellenleiter.lower()
                        jobcomment = job.comment.lower()
                        companyname = company.name.lower()                
                    if self.ui.filterCalendar.isChecked():
                        daySpace = self.calcDaySpace(job.startdate,  job.enddate, wcm,  job.weekendDays)
                    #cal + search
                    if self.ui.filterCalendar.isChecked() and self.ui.filterInactive.isChecked() and infoSearch != "":
                        if (((job.startdate.month() == wcm) and (job.startdate.year() == wcy)) or (((job.enddate.month() == wcm)) and (job.enddate.year()== wcy)))and (re.search(infoSearch,  jobname) is not None  or re.search(infoSearch,  jobplace) is not None or re.search(infoSearch,  jobcomment) is not None or re.search(infoSearch,  jobleader) is not None or re.search(infoSearch, companyname) is not None):
                            self.createJobRow(job, company, rowNr, wcm,  daySpace) 
                            insertARow = True
                            rowNr = rowNr + 1
                            self.ui.infoExel.insertRow(rowNr)
                    #cal +inactive + search
                    if self.ui.filterCalendar.isChecked() and self.ui.filterInactive.isChecked() == False and infoSearch != "":
                        if (((job.startdate.month() == wcm) and (job.startdate.year() == wcy)) or (((job.enddate.month() == wcm)) and (job.enddate.year()== wcy)))and (re.search(infoSearch,  jobname) is not None  or re.search(infoSearch,  jobplace) is not None or re.search(infoSearch,  jobcomment) is not None or re.search(infoSearch,  jobleader) is not None or re.search(infoSearch, companyname) is not None) and job.active == 1:
                            self.createJobRow(job, company, rowNr, wcm,  daySpace) 
                            insertARow = True
                            rowNr = rowNr + 1
                            self.ui.infoExel.insertRow(rowNr)
                    #search
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
                            insertARow = True
                    #----- no filters (but filter@all)
                    elif self.ui.filterCalendar.isChecked() == False and self.ui.filterInactive.isChecked() and infoSearch == "":
                        self.createJobRow(job, company, rowNr, wcm,  daySpace)  
                        rowNr = rowNr + 1
                        self.ui.infoExel.insertRow(rowNr)
                        insertARow = True
                    #calendar
                    elif self.ui.filterCalendar.isChecked() and self.ui.filterInactive.isChecked() and infoSearch == "":
                        if ((job.startdate.month() == wcm) and (job.startdate.year() == wcy)) or (((job.enddate.month() == wcm)) and (job.enddate.year()== wcy)):
                          self.createJobRow(job, company, rowNr, wcm,  daySpace)  
                          rowNr = rowNr + 1
                          self.ui.infoExel.insertRow(rowNr)
                          insertARow = True
                    #inactive calendar
                    elif self.ui.filterCalendar.isChecked() and self.ui.filterInactive.isChecked() == False and infoSearch == "":
                        if (((job.startdate.month() == wcm) and (job.startdate.year() == wcy)) or ((job.enddate.month() == wcm)) and (job.enddate.year()== wcy) and job.active == 1):
                            self.createJobRow(job, company, rowNr,  wcm,  daySpace)
                            rowNr = rowNr + 1
                            self.ui.infoExel.insertRow(rowNr)
                            insertARow = True
                    #inactive
                    elif self.ui.filterCalendar.isChecked() ==False and self.ui.filterInactive.isChecked() == False and infoSearch == "":
                        if  job.active == 1:
                            self.createJobRow(job, company, rowNr,  wcm,  daySpace)
                            rowNr = rowNr + 1
                            self.ui.infoExel.insertRow(rowNr)
                            insertARow = True
                    #inactive + search
                    elif self.ui.filterCalendar.isChecked() ==False and self.ui.filterInactive.isChecked() == False and infoSearch != "":
                        if  (re.search(infoSearch,  jobname) is not None  or re.search(infoSearch,  jobplace) is not None or re.search(infoSearch,  jobcomment) is not None or re.search(infoSearch,  jobleader) is not None or re.search(infoSearch,  companyname) is not None) and job.active == 1:
                            self.createJobRow(job, company, rowNr,  wcm,  daySpace)
                            rowNr = rowNr + 1
                            self.ui.infoExel.insertRow(rowNr)
                            insertARow = True
                else:
                    self.createJobRow(job, company,rowNr,  wcm,  daySpace)
                    rowNr = rowNr + 1
                    self.ui.infoExel.insertRow(rowNr)
                    insertARow = True
            creditSum = 0
            if insertARow:
                #change to check credit-list-size
                for credit in company.credits:
                    if (self.ui.filterCalendar.isChecked() and credit.date.month() == wcm and credit.date.year() == wcy) or self.ui.filterCalendar.isChecked() == False:
                        creditSum += credit.value
                        creditString += "- "+credit.date.toString(dbDateFormat)+": "+str(credit.value)+"<br />"
                if creditSum > 0:
                    creditString += "------------<br />"+tr("Creditsum", "Creditsum")+ ":"+str(creditSum)
            self.ui.infoExelCredits.setText(creditString)
            self.sum -= creditSum
            self.ui.amount.display(self.sum)
    def createJobRow(self,  job, company, rowNr,  wcm,  daySpace):
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
        self.sum = self.sum + loanSum
        #building table..
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(company.name) ))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(job.name) ))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(job.place) ))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(job.baustellenleiter) ))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(self.rounder(loanSum) + ".- ("+self.rounder(realLoan)+"/std)" ))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(self.rounder(hrSpace) +" Std / "+self.rounder(daySpace)+ "d (*"+str(job.hours)+"h)"))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(self.rounder(spesenSum)+".- " ))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(self.rounder(loanSplitSum)+".- ("+self.rounder(realLoanSplitSum)+".- @all)" ))
        colNr = colNr + 1
        self.ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(self.rounder(self.sum)+".-" ))
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
    def updateCompanyViewList(self):
        self.ui.companyViewList.clear()
        for company in mightyController.companylist:
            self.ui.companyViewList.addItem(company.name)
    def updateCompanyView(self):
        ccm = self.ui.companyViewCalendar.monthShown()
        ccy = self.ui.companyViewCalendar.yearShown()
        for company in mightyController.companylist:
            if self.ui.companyViewList.currentText() == company.name:
                text = ""
                text += "<h1>"+company.name+"</h1>"+company.describtion+"<br />"+tr("Loan", "Loan")+": "+str(company.loan)+" (per "+str(company.perHours)+"h)<hr />"
                loanSplitSum = 0
                #LoanSplits
                text += "<ul>"
                for ls in  company.loanSplits:
                    text += "<li>"+ls.name+": "+str(ls.value)
                    if ls.money:
                        loanSplitSum += ls.value
                        text += ".- </li>"
                    else:
                        inMoney = (company.loan / 100) * ls.value
                        loanSplitSum += inMoney
                        text += "% ("+self.rounder(inMoney)+".-) </li>"
                text += "</ul>"
                if loanSplitSum > 0:
                    text += tr("Loansplitsum", "")+": "+self.rounder(loanSplitSum)+".-<hr />"
                creditSum = 0
                text += "<ul>"
                for credit in company.credits:
                    if (credit.date.month() == ccm and credit.date.year() == ccy) or  self.ui.companyViewCalendarFilter.isChecked() == False:
                        creditSum += credit.value
                        text += "<li>"+credit.date.toString(dbDateFormat) + ": "+str(credit.value)+""
                        if credit.payed:
                            text +=".- is"+tr("payed", "")+"</li>"
                        else:
                            text +=".- is"+tr("payed", "")+"</li>"
                text += "</ul>"
                if creditSum > 0:
                    text += tr("Creditsum", "")+": "+self.rounder(creditSum)+".- <hr />"
                jobSum = 0
                jobDays = 0
                jobHours = 0
                chargeSum = 0
                text += "<ul>"
                for job in company.jobs:
                    if self.ui.companyViewCalendarFilter.isChecked():
                        if (job.startdate.month() == ccm and job.startdate.year() == ccy) or (job.enddate.month() == ccm and job.startdate.year() == ccy):
                            days = self.calcDaySpace(job.startdate,  job.enddate, ccm,  job.weekendDays)
                        else:
                            days = -1
                    else:
                        days = job.startdate.daysTo(job.enddate) + 1
                    if days != -1:
                        jobDays += days
                       
                        hourSpace = days * (job.hours / company.perHours ) +job.correctionHours
                        jobHours += hourSpace
                        jobSum += company.loan * hourSpace
                        text += "<li>"+job.name+": "+str(days)+"d * ("+str(job.hours)+"h /"+str(company.perHours)+" )+" +str(job.correctionHours)+"h = "+str(hourSpace)+"h * " + str(company.loan)+".-  ="+str(hourSpace*company.loan)+".- </li>"
                        text += "<ul>"
                        for charge in job.wcharges:
                            chargeSum += charge.value *  days
                            text += "<li>"+charge.name+": "+str(charge.value)+".- * "+str(days)+"d = "+str(charge.value * days)+".- </li>"
                        text += "</ul>"
                text += "</ul> Sum: "+str(jobSum)+".- in "+str(jobHours)+"h / "+str(jobDays )+" d (+ "+str(chargeSum)+".- charges) <hr />"
                loanSplitSumDays = loanSplitSum * jobDays
                result = jobSum - loanSplitSumDays - creditSum + chargeSum
                #the end of all results..
                text += "<ul><li><b>"+self.rounder(jobSum)+".-</b> </li><li><b> - "+self.rounder(loanSplitSumDays)+".-  </b>"+tr("Splits", "")+"</li><li><b> - "+self.rounder(creditSum)+".- </b>"+tr(  "Credits", "")+"</li> <li><b> + "+self.rounder(chargeSum)+".- </b> "+tr("Charges", "")+"</li></ul><hr /> "+tr("Your company should pay", "")+"<b> "+self.rounder(result)+".- </b>"
                self.ui.companyViewText.setText(text)
                

app = QtGui.QApplication(sys.argv)
lang = ""
for config in mightyController.configlist:
    if config.key == "lang" or config.key == "language":
        lang=config.value
translator = QtCore.QTranslator()
translator.load(lang,"./")
app.installTranslator(translator)
jobman = Gui()
jobman.show()

sys.exit(app.exec_())
