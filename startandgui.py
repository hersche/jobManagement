#this code is GPL-FORCED so let changes open, pls!!
#License @ http://www.gnu.org/licenses/gpl.txt
#Author: skamster

import os.path,  sys,  re
from PyQt4 import QtGui, QtCore
from models import *

    
def tr(name, bla=""):
    return QtCore.QCoreApplication.translate("@default",  name)
singleView = False
singleViewId = -1
singleViewName = ""
mightyController = Controller();
for config in mightyController.configlist:
    if (config.key.lower() == "single" or config.key.lower() == "singleview") and (config.value.lower() == "true" or config.value.lower() == "1"):
        singleView = True
        from gui_single import Ui_MainWindowSingle
    elif config.key.lower()== "singleciewcname":
        singleViewName = config.value
    elif config.key.lower()== "singleciewcid":
        singleViewId = config.value
if True is not singleView:
    from gui import Ui_MainWindow
class Gui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        # INIT

        self.showInactive = True
        QtGui.QWidget.__init__(self, parent)
        if singleView:
            self.ui = Ui_MainWindowSingle()
        else:
            self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        if singleView:
            #init self.currentCompany
            self.onCompanyItemClick("singleView")
        self.updateInfoExel()
        cd = QtCore.QDate.currentDate()
        if singleView == False:
            self.ui.startdate.setDate(cd)
            self.ui.enddate.setDate(cd)
        self.ui.creditDate.setDate(cd)
        self.updateCompanyList(True)
        self.updateInfoExel()
        self.updateCompanyView()
        self.updateConfigList()
        self.updatePersonalChargesList()
        self.updatePersonalCreditList()
        self.alertBox = QtGui.QMessageBox()
        
        #-----------------------
        #Data-Tab
        #-----------------------
        #Item-Clicks
        if not singleView:
            self.ui.companyList.itemClicked.connect(self.onCompanyItemClick)
        self.ui.jobList.itemClicked.connect(self.onJobItemClick)
        self.ui.creditList.itemClicked.connect(self.onCreditItemClick)
        self.ui.chargesList.itemClicked.connect(self.onSpeseItemClick)
        self.ui.personalCreditList.itemClicked.connect(self.onPersonalCreditItemClick)
        self.ui.personalChargesList.itemClicked.connect(self.onPersonalChargeItemClick)
        self.ui.loanSplitList.itemClicked.connect(self.onLoanSplitItemClick)
        self.ui.configList.itemClicked.connect(self.onConfigItemClick)
        self.ui.workChargesList.itemClicked.connect(self.onWChargeItemClick)

        #Company-Actions
        if not singleView:
            self.ui.createCompany.clicked.connect(self.onCreateCompany)
            self.ui.deleteCompany.clicked.connect(self.onDeleteCompany)
        self.ui.saveCompany.clicked.connect(self.onSaveCompany)
        
        #Job-Actions
        self.ui.createJob.clicked.connect(self.onCreateJob)
        self.ui.saveJob.clicked.connect(self.onSaveJob)
        self.ui.deleteJob.clicked.connect(self.onDeleteJob)
        #Charge-Actions
        self.ui.createCharge.clicked.connect(self.onCreateSpese)
        self.ui.saveCharge.clicked.connect(self.onSaveSpese)
        self.ui.deleteCharge.clicked.connect(self.onDeleteSpese)
        self.ui.deleteWorkSpese.clicked.connect(self.onDeleteWorkSpese)
        self.ui.addChargeToJob.clicked.connect(self.onAddWorkSpese)
        self.ui.wChargeSave.clicked.connect(self.onSaveWorkSpese)
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
        #---------------------
        #personal tab
        #---------------------
        #Charge-Actions
        self.ui.createPersonalCharge.clicked.connect(self.onCreatePersonalCharge)
        self.ui.savePersonalCharge.clicked.connect(self.onSavePersonalCharge)
        self.ui.deletePersonalCharge.clicked.connect(self.onDeletePersonalCharge)

        #Credit-Actions
        self.ui.createPersonalCredit.clicked.connect(self.onCreatePersonalCredit)
        self.ui.savePersonalCredit.clicked.connect(self.onSavePersonalCredit)
        self.ui.deletePersonalCredit.clicked.connect(self.onDeletePersonalCredit)
        
        
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
        if not singleView:
            self.ui.companyViewList.currentIndexChanged.connect(self.updateCompanyView)
        self.ui.companyViewCalendar.currentPageChanged.connect(self.updateCompanyView)
        self.ui.companyViewCalendarFilter.clicked.connect(self.updateCompanyView)
    
    
    #----------------------
    # Updaters
    #-----------------------
    def updateCompanyList(self, selectFirst=False):
        
        if singleView == False:
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
    def updatePersonalChargesList(self,  selectFirst=False,  name=""):
        self.ui.personalChargesList.clear()
        mightyController.updatePersonalChargesList()
        for spese in mightyController.personalCharges:
            self.ui.personalChargesList.addItem(spese.name)
        if selectFirst:
            self.ui.personalChargesList.setCurrentRow(0)
            self.onPersonalChargeItemClick(self.ui.personalChargesList.currentItem())
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
            self.ui.creditList.addItem(credit.name+" / "+str(credit.value) +".- "+credit.date.toString(dbDateFormat))
        if selectFirst:
            self.ui.creditList.setCurrentRow(0)
            self.onCreditItemClick(self.ui.creditList.currentItem())
    def updatePersonalCreditList(self,  selectFirst=False, valueDate=""):
        self.ui.personalCreditList.clear()
        mightyController.updatePersonalCreditList()
        for credit in mightyController.personalCredits:
            #if valueDate is not "" and valueDate == str(credit.value) +" "+credit.date:
            self.ui.personalCreditList.addItem(credit.name+" / "+str(credit.value) +".- "+credit.date.toString(dbDateFormat))
        if selectFirst:
            self.ui.personalCreditList.setCurrentRow(0)
            self.onPersonalCreditItemClick(self.ui.personalCreditList.currentItem())
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
        if singleView:
            if singleViewId != -1:
                self.currentCompany = mightyController.getCompanyById(singleViewId)
            elif singleViewName != "":
                self.currentCompany = mightyController.getCompanyByName(singleViewName)
            else:
                self.currentCompany = mightyController.getCompanyById(1)
        else:
            for company in mightyController.companylist:
                if company.name == item.text():
                    self.currentCompany = company
        self.ui.companyname.setText(self.currentCompany.name)
        self.ui.loan.setValue(self.currentCompany.loan)
        if not singleView:
            self.ui.companydescription.clear()
            self.ui.perHours.setValue(self.currentCompany.perHours)
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
    def onPersonalChargeItemClick(self, item):
        for spese in mightyController.personalCharges:
            if spese.name == item.text():
                self.ui.personalChargesName.setText(spese.name)
                self.ui.personalChargesValue.setValue(spese.value)
    def onWChargeItemClick(self, item):
        jobSelect = self.ui.jobList.currentItem()
        for  job in self.currentCompany.jobs:
            if job.name == jobSelect.text():
                for charge in job.wcharges:
                    if charge.name == item.text():
                        self.ui.wChargeTimes.setValue(charge.howManyTimes)
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
            if item is not None and (credit.name+" / "+str(credit.value) +".- "+credit.date.toString(dbDateFormat)) == item.text():
                self.ui.creditName.setText(credit.name)
                self.ui.creditValue.setValue(credit.value)
                self.ui.creditDate.setDate(credit.date)
                if credit.payed:
                    self.ui.creditPayed.setChecked(True)
                else:
                    self.ui.creditPayed.setChecked(False)
                if credit.active:
                    self.ui.creditActive.setChecked(True)
                else:
                    self.ui.creditActive.setChecked(False)
    def onPersonalCreditItemClick(self, item):
        for credit in mightyController.personalCredits:
            if item is not None and (credit.name+" / "+str(credit.value) +".- "+credit.date.toString(dbDateFormat)) == item.text():
                self.ui.personalCreditName.setText(credit.name)
                self.ui.personalCreditValue.setValue(credit.value)
                self.ui.personalCreditDate.setDate(credit.date)
                if credit.payed:
                    self.ui.personalCreditPayed.setChecked(True)
                else:
                    self.ui.personalCreditPayed.setChecked(False)
                if credit.active:
                    self.ui.personalCreditActive.setChecked(True)
                else:
                    self.ui.personalCreditActive.setChecked(False)
    def onJobItemClick(self,  item):
        for job in self.currentCompany.jobs:
            if item is not None and item.text() == job.name:
                self.currentJob = job
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
                if singleView == False:
                    self.ui.startdate.setDate(job.startdate)
                    self.ui.enddate.setDate(job.enddate)
                    self.ui.daysCalc.setText(str(job.startdate.daysTo(job.enddate)+1)+ " "+ tr("days"))
                    self.ui.hoursCalc.setText(str((job.startdate.daysTo(job.enddate)+1)*job.hours)+" "+ tr(" hours"))
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
        success = False
        for spese in self.currentCompany.charges:
            if cm is not None and spese.name == cm.text():
                spese.save(self.ui.chargesName.text(), self.ui.chargesValue.text())
                success = True
                self.ui.status.setText(tr("Charge")+" "+self.ui.chargesName.text()+" "+tr("saved"))
        if not success:
            self.alertBox.setText(tr("Charge")+" "+tr("could not")+" be "+tr("saved"))
            self.alertBox.exec()
        else:
            self.updatechargesList(True)
            self.updateWorkchargesList(True)
            self.ui.chargesList.setCurrentRow(cr)
            self.ui.chargesList.setCurrentItem(cm)
    def onDeleteSpese(self):
        cm = self.ui.chargesList.currentItem()
        success = False
        for spese in self.currentCompany.charges:
            if cm is not None and spese.name == cm.text():
                spese.delete()
                success = True
                self.ui.status.setText(tr("Charge")+" "+cm.text()+" "+tr("deleted"))
        if not success:
            self.alertBox.setText(tr("Charge")+" "+tr("could not")+" be "+tr("deleted"))
            self.alertBox.exec()
        else:
            self.updatechargesList(True)
    #-------------
    # PersonalCharges-Actions
    #--------------
    def onCreatePersonalCharge(self):
        self.currentCompany.createSpese(self.ui.personalChargesName.text(), self.ui.personalChargesValue.text(), -1)
        # @TODO select the created!
        self.updatePersonalChargesList(True)
    def onSavePersonalCharge(self):
        cr = self.ui.personalChargesList.currentRow()
        cm = self.ui.personalChargesList.currentItem()
        success = False
        for spese in mightyController.personalCharges:
            if cm is not None and spese.name == cm.text():
                spese.save(self.ui.personalChargesName.text(), self.ui.personalChargesValue.text())
                success = True
                self.ui.status.setText(tr("PersonalCharge")+" "+self.ui.personalChargesName.text()+" "+tr("saved"))
        self.updatePersonalChargesList(True)
        self.ui.personalChargesList.setCurrentRow(cr)
        if not success:
            self.alertBox.setText(tr("PersonalCharge")+" "+tr("could not")+" be "+tr("saved"))
            self.alertBox.exec()
        self.ui.personalChargesList.setCurrentItem(cm)
    def onDeletePersonalCharge(self):
        cm = self.ui.personalChargesList.currentItem()
        success = False
        for spese in mightyController.personalCharges:
            if cm is not None and spese.name == cm.text():
                spese.delete()
                success = True
                self.ui.status.setText(tr("Charge")+" "+cm.text()+" "+tr("deleted"))
        if not success:
            self.alertBox.setText(tr("Charge")+" "+tr("could not")+" be "+tr("deleted"))
            self.alertBox.exec()
        else:
            self.updatePersonalChargesList(True)
    #-------------
    # loanSplit-Actions
    #--------------
    def onCreateLoanSplit(self):
        self.currentCompany.createLoanSplit(self.ui.loanSplitName.text(), self.ui.loanSplitValue.text(),  self.ui.loanSplitMoney.isChecked())
        # @TODO select the created!
        self.ui.status.setText(tr("LoanSplit")+" "+self.ui.loanSplitName.text()+" "+tr("created"))
        self.updateLoanSplitList(True)
    def onSaveLoanSplit(self):
        cr = self.ui.loanSplitList.currentRow()
        cm = self.ui.loanSplitList.currentItem()
        success = False
        for loanSplit in self.currentCompany.loanSplits:
            if cm is not None and loanSplit.name == cm.text():
                loanSplit.save(self.ui.loanSplitName.text(), self.ui.loanSplitValue.text(),  self.ui.loanSplitMoney.isChecked())
                success = True
                self.ui.status.setText(tr("LoanSplit")+" "+self.ui.loanSplitName.text()+" "+tr("saved"))
        if not success:
            self.alertBox.setText(tr("LoanSplit")+" "+tr("could not")+" be "+tr("saved"))
            self.alertBox.exec()
        else:
            self.updateLoanSplitList()
            self.ui.loanSplitList.setCurrentRow(cr)
            self.ui.loanSplitList.setCurrentItem(cm)
    def onDeleteLoanSplit(self):
        cm = self.ui.loanSplitList.currentItem()
        success = False
        for loanSplit in self.currentCompany.loanSplits:
            if cm is not None and loanSplit.name == cm.text():
                loanSplit.delete()
                success = True
                self.ui.status.setText(tr("LoanSplit")+" "+cm.text()+" "+tr("deleted"))
        if not success:
            self.alertBox.setText(tr("Charge")+" "+tr("could not")+" be "+tr("saved"))
            self.alertBox.exec()
        else:
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
        success = False
        for config in mightyController.configlist:
            if cm is not None and config.key == cm.text():
                config.save(self.ui.configKey.text(), self.ui.configValue.text())
                success = True
                self.ui.status.setText(tr("Config")+" "+self.ui.configKey.text()+" "+tr("saved"))
        if not success:
            self.alertBox.setText(tr("Charge")+" "+tr("could not")+" be "+tr("saved"))
            self.alertBox.exec()
        else:
            self.updateConfigList()
            self.ui.configList.setCurrentRow(cr)
            self.ui.configList.setCurrentItem(cm)
    def onDeleteConfig(self):
        cm = self.ui.configList.currentItem()
        success = False
        for config in mightyController.configlist:
            if cm is not None and config.key == cm.text():
                config.delete()
                success = True
                self.ui.status.setText(tr("Charge")+" "+cm.text()+" "+tr("deleted"))
        if not success:
            self.alertBox.setText(tr("Charge")+" "+tr("could not")+" be "+tr("saved"))
            self.alertBox.exec()
        else:
            self.updateConfigList(True)
        
    #---------------------------------------
    # Credit-Actions
    #---------------------------------------
    def onCreateCredit(self):
        self.currentCompany.createCredit(self.ui.creditName.text(), self.ui.creditValue.value(), self.ui.creditDate.text(), self.ui.creditPayed.isChecked(), self.ui.creditActive.isChecked())
        self.ui.status.setText(tr("Credit")+" "+tr("created")+":"+str(self.ui.creditValue.value()))
        # @TODO select the created!
        self.updateCreditList(selectFirst=True)
    def onSaveCredit(self):
        success = False
        cr = self.ui.creditList.currentRow()
        cm = self.ui.creditList.currentItem()
        for credit in self.currentCompany.credits:
            if cm is not None and (credit.name+" / "+str(credit.value) +".- "+credit.date.toString(dbDateFormat)) == cm.text():
                credit.save(self.ui.creditName.text(), self.ui.creditValue.text(), self.ui.creditDate.text(),   self.ui.creditPayed.isChecked(), self.ui.creditActive.isChecked())
                success = True
                self.ui.status.setText(tr("Credit")+" "+self.ui.creditName.text()+":"+self.ui.creditValue.text()+" "+tr("saved"))
        if not success:
            self.alertBox.setText(tr("Credit")+" "+tr("could not")+" be "+tr("saved"))
            self.alertBox.exec()
        else:
            self.updateCreditList()
            self.ui.creditList.setCurrentRow(cr)
    def onDeleteCredit(self):
        success = False
        cm = self.ui.creditList.currentItem()
        for credit in self.currentCompany.credits:
            if cm is not None and (credit.name+" / "+str(credit.value) +".- "+credit.date.toString(dbDateFormat)) == cm.text():
                credit.delete()
                success = True
                self.ui.status.setText(tr("Credit")+" "+self.ui.creditValue.text()+" "+tr("deleted"))
        if not success:
            self.alertBox.setText(tr("Credit")+" "+tr("could not")+" be "+tr("deleted"))
            self.alertBox.exec()
        else:
            self.updateCreditList(True)
        
    #---------------------------------------
    # personalCredit-Actions
    #---------------------------------------
    def onCreatePersonalCredit(self):
        self.currentCompany.createCredit(self.ui.personalCreditName.text(), self.ui.personalCreditValue.value(), self.ui.personalCreditDate.text(), self.ui.personalCreditPayed.isChecked(), self.ui.personalCreditActive.isChecked(), -1)
        self.ui.status.setText(tr("Credit")+" "+tr("created")+":"+str(self.ui.personalCreditValue.value()))
        # @TODO select the created!
        self.updatePersonalCreditList(selectFirst=True)
    def onSavePersonalCredit(self):
        cr = self.ui.personalCreditList.currentRow()
        cm = self.ui.personalCreditList.currentItem()
        success = False
        for credit in mightyController.personalCredits:
            if cm is not None and (credit.name+" / "+str(credit.value) +".- "+credit.date.toString(dbDateFormat)) == cm.text():
                credit.save(self.ui.personalCreditName.text(), self.ui.personalCreditValue.text(), self.ui.personalCreditDate.text(),   self.ui.personalCreditPayed.isChecked(), self.ui.personalCreditActive.isChecked())
                success = True
                self.ui.status.setText(tr("Personal credit")+" "+self.ui.creditName.text()+":"+self.ui.creditValue.text()+" "+tr("saved"))
        if not success:
            self.alertBox.setText(tr("Personal credit")+" "+tr("could not")+" be "+tr("deleted"))
            self.alertBox.exec()
        else:
            self.updatePersonalCreditList()
            self.ui.personalCreditList.setCurrentRow(cr)
    def onDeletePersonalCredit(self):
        cm = self.ui.personalCreditList.currentItem()
        success = False
        for credit in mightyController.personalCredits:
            if cm is not None and (credit.name+" / "+str(credit.value) +".- "+credit.date.toString(dbDateFormat))== cm.text():
                credit.delete()
                success = True
                self.ui.status.setText(tr("Personal buying")+" "+self.ui.personalCreditValue.text()+" "+tr("deleted"))
        if not success:
            self.alertBox.setText(tr("Personal buying")+" "+tr("could not")+" be "+tr("deleted"))
            self.alertBox.exec()
        else:
            self.updatePersonalCreditList(True)
        
        
    #--------------------
    # Company-Actions
    #---------------------
    def onCreateCompany(self):
        mightyController.createCompany(self.ui.companyname.text(),  self.ui.loan.text(),  self.ui.perHours.text(),  self.ui.companydescription.toPlainText())
        self.ui.companyList.addItem(self.ui.companyname.text())
    def onSaveCompany(self):
        if self.currentCompany is not None:
            if singleView:
                self.currentCompany.save(self.ui.companyname.text(),  self.ui.loan.text(), 1, "SingleViewCompany")
            else:
                self.currentCompany.save(self.ui.companyname.text(),  self.ui.loan.text(), self.ui.perHours.text(), self.ui.companydescription.toPlainText())
        else:
            self.alertBox.setText("Company could not be saved")
            self.alertBox.exec()
        self.updateCompanyList()
    def onDeleteCompany(self):
        if self.currentCompany is not None:
            self.currentCompany.delete()
        else:
            self.alertBox.setText("Company could not be deleted")
            self.alertBox.exec()
        self.updateCompanyList(True)
        
        
    #------------------------
    # Job-Actions
    #------------------------
    def onCreateJob(self):
        tmpCheck = 0
        if self.ui.active.isChecked():
            tmpCheck = 1
        if singleView:
            self.currentCompany.createJob(self.ui.jobname.text(), self.ui.jobplace.text(), self.ui.jobComment.toPlainText(), self.ui.hours.text(),self.ui.correctionHours.text(),  self.ui.weekendDays.value(),  -1,  -1,  self.ui.baustellenleiter.text(),  tmpCheck)
        else:
            self.currentCompany.createJob(self.ui.jobname.text(), self.ui.jobplace.text(), self.ui.jobComment.toPlainText(), self.ui.hours.text(),self.ui.correctionHours.text(),  self.ui.weekendDays.value(),  self.ui.startdate.text(),  self.ui.enddate.text(),  self.ui.baustellenleiter.text(),  tmpCheck)
        # @TODO select the created!!
        self.ui.jobList.addItem(self.ui.jobname.text())
    def onSaveJob(self):
        cm = self.ui.jobList.currentItem()
        for job in self.currentCompany.jobs:
            if  cm is not None and job.name == str(cm.text()):
                # name,  place,  startdate, enddate, baustellenleiter, active, companyid
                if singleView:
                    job.save(self.ui.jobname.text(),  self.ui.jobplace.text(),self.ui.jobComment.toPlainText(),   self.ui.hours.text(),self.ui.correctionHours.text(),  self.ui.weekendDays.value(),-1, -1, self.ui.baustellenleiter.text(),  self.ui.active.isChecked(), self.currentCompany.id)
                else:
                    job.save(self.ui.jobname.text(),  self.ui.jobplace.text(),self.ui.jobComment.toPlainText(),   self.ui.hours.text(),self.ui.correctionHours.text(),  self.ui.weekendDays.value(),  self.ui.startdate.text(),  self.ui.enddate.text(),  self.ui.baustellenleiter.text(),  self.ui.active.isChecked(), self.currentCompany.id)
                self.ui.status.setText("Job "+job.name+" "+tr("saved"))
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
    def onSaveWorkSpese(self):
        cs = self.ui.workChargesList.currentItem()
        cm = self.ui.jobList.currentItem()
        for job in self.currentCompany.jobs: 
            if  cm is not None and job.name == str(cm.text()):
                job.saveCharge(cs.text(),  self.ui.wChargeTimes.value())
        self.updateWorkchargesList(True)
    def onAddWorkSpese(self):
        cs = self.ui.chargesList.currentItem()
        cm = self.ui.jobList.currentItem()
        for job in self.currentCompany.jobs:
            if  cm is not None and job.name == cm.text():
                for spese in self.currentCompany.charges:
                    if cs is not None and spese.name == cs.text():
                        job.addSpese(spese.id,  self.ui.wChargeTimes.value())
                        job.updateWchargesList()
        self.updateWorkchargesList()
    def rounder(self, nr):
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
    def calcDaySpace(self,  startdate,  enddate,  cm,  weekendDays):
        if startdate.month() != enddate.month():
            allDays = startdate.daysTo(enddate)
            if startdate.month() == cm:
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
        self.ui.infoExel.insertRow(0)
        self.ui.infoExel.insertRow(1)
        self.ui.infoExel.insertRow(2)
        self.ui.infoExel.insertRow(3)
        #proof of concept, have to move..
        self.updateGraphicView()
        self.updateCompanyViewList()
        rowNr = 0
        self.sum = 0
        if singleView:
            self.ui.infoExel.setHorizontalHeaderLabels((tr( "Jobname"),tr( "Place"), tr( "Leader"), tr( "Loan"),tr( "Time"), tr(  "Charges"), tr( "Splits"), tr( "Summe")))
        else:
            self.ui.infoExel.setHorizontalHeaderLabels((tr( "Companyname"),tr( "Jobname"),tr( "Place"), tr( "Leader"), tr( "Loan"),tr( "Time"), tr(  "Charges"), tr( "Splits"), tr( "Summe")))
        wcm = self.ui.workCalendar.monthShown()
        wcy = self.ui.workCalendar.yearShown()
        infoSearch = self.ui.infoSearch.text()
        infoSearch = infoSearch.lower()
        if singleView:
            company = self.currentCompany
            self.filterJobs(self.currentCompany, infoSearch,  wcm, wcy, rowNr)
            self.createCreditTextBox(self.currentCompany, wcm, wcy)
        else:
            for company in mightyController.companylist:
                self.ui.infoExel.insertRow(rowNr)
                self.filterJobs(company, infoSearch,  wcm, wcy, rowNr)
                rowNr += 1
                self.createCreditTextBox(company, wcm, wcy)


    def createCreditTextBox(self, company, wcm, wcy):
        creditString =""
        creditSum = 0
        #change to check credit-list-size
        for credit in company.credits:
            if (self.ui.filterCalendar.isChecked() and credit.date.month() == wcm and credit.date.year() == wcy) or self.ui.filterCalendar.isChecked() == False:
                creditSum += credit.value
                creditString += "- "+credit.date.toString(dbDateFormat)+": "+str(credit.value)+"<br />"
        if creditSum > 0:
            creditString += "------------<br />"+tr("Creditsum")+ ":"+str(creditSum)
        self.ui.infoExelCredits.setText(creditString)
        self.sum -= creditSum
        self.ui.amount.display(self.sum)
    def filterJobs(self, company, infoSearch, wcm, wcy, rowNr):
        for job in company.jobs:
            #insertARow = False
            if singleView:
                daySpace = 30
            else:
                daySpace = job.startdate.daysTo(job.enddate) + 1
            if self.ui.filterAll.isChecked():
                #prepares
                if self.ui.infoSearch.text() != "":
                    jobname = job.name.lower()
                    jobplace = job.place.lower()
                    jobleader = job.baustellenleiter.lower()
                    jobcomment = job.comment.lower()
                    companyname = company.name.lower()                
                if self.ui.filterCalendar.isChecked():
                    if singleView:
                        daySpace = 30
                    else:
                        daySpace = self.calcDaySpace(job.startdate,  job.enddate, wcm,  job.weekendDays)
                #cal + search
                if self.ui.filterCalendar.isChecked() and self.ui.filterInactive.isChecked() and infoSearch != "":
                    if (((job.startdate.month() == wcm) and (job.startdate.year() == wcy)) or (((job.enddate.month() == wcm)) and (job.enddate.year()== wcy)))and (re.search(infoSearch,  jobname) is not None  or re.search(infoSearch,  jobplace) is not None or re.search(infoSearch,  jobcomment) is not None or re.search(infoSearch,  jobleader) is not None or re.search(infoSearch, companyname) is not None):
                        self.createJobRow(job, company, rowNr, wcm,  daySpace) 
                        #insertARow = True
                        rowNr = rowNr + 1
                        self.ui.infoExel.insertRow(rowNr)
                #cal +inactive + search
                if self.ui.filterCalendar.isChecked() and self.ui.filterInactive.isChecked() == False and infoSearch != "":
                    if (((job.startdate.month() == wcm) and (job.startdate.year() == wcy)) or (((job.enddate.month() == wcm)) and (job.enddate.year()== wcy)))and (re.search(infoSearch,  jobname) is not None  or re.search(infoSearch,  jobplace) is not None or re.search(infoSearch,  jobcomment) is not None or re.search(infoSearch,  jobleader) is not None or re.search(infoSearch, companyname) is not None) and job.active == 1:
                        self.createJobRow(job, company, rowNr, wcm,  daySpace) 
                        #insertARow = True
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
                        #insertARow = True
                #----- no filters (but filter@all)
                elif self.ui.filterCalendar.isChecked() == False and self.ui.filterInactive.isChecked() and infoSearch == "":
                    self.createJobRow(job, company, rowNr, wcm,  daySpace)  
                    rowNr = rowNr + 1
                    self.ui.infoExel.insertRow(rowNr)
                    #insertARow = True
                #calendar
                elif self.ui.filterCalendar.isChecked() and self.ui.filterInactive.isChecked() and infoSearch == "":
                    if ((job.startdate.month() == wcm) and (job.startdate.year() == wcy)) or (((job.enddate.month() == wcm)) and (job.enddate.year()== wcy)):
                      self.createJobRow(job, company, rowNr, wcm,  daySpace)  
                      rowNr = rowNr + 1
                      self.ui.infoExel.insertRow(rowNr)
                      #insertARow = True
                #inactive calendar
                elif self.ui.filterCalendar.isChecked() and self.ui.filterInactive.isChecked() == False and infoSearch == "":
                    if (((job.startdate.month() == wcm) and (job.startdate.year() == wcy)) or ((job.enddate.month() == wcm)) and (job.enddate.year()== wcy) and job.active == 1):
                        self.createJobRow(job, company, rowNr,  wcm,  daySpace)
                        rowNr = rowNr + 1
                        self.ui.infoExel.insertRow(rowNr)
                        #insertARow = True
                #inactive
                elif self.ui.filterCalendar.isChecked() ==False and self.ui.filterInactive.isChecked() == False and infoSearch == "":
                    if  job.active == 1:
                        self.createJobRow(job, company, rowNr,  wcm,  daySpace)
                        rowNr = rowNr + 1
                        self.ui.infoExel.insertRow(rowNr)
                        #insertARow = True
                #inactive + search
                elif self.ui.filterCalendar.isChecked() ==False and self.ui.filterInactive.isChecked() == False and infoSearch != "":
                    if  (re.search(infoSearch,  jobname) is not None  or re.search(infoSearch,  jobplace) is not None or re.search(infoSearch,  jobcomment) is not None or re.search(infoSearch,  jobleader) is not None or re.search(infoSearch,  companyname) is not None) and job.active == 1:
                        self.createJobRow(job, company, rowNr,  wcm,  daySpace)
                        rowNr = rowNr + 1
                        self.ui.infoExel.insertRow(rowNr)
                        #insertARow = True
            else:
                self.createJobRow(job, company,rowNr,  wcm,  daySpace)
                rowNr = rowNr + 1
                self.ui.infoExel.insertRow(rowNr)
                #insertARow = True
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
        if not singleView:
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
        if singleView == False:
            self.ui.companyViewList.clear()
            for company in mightyController.companylist:
                self.ui.companyViewList.addItem(company.name)
    def updateCompanyView(self):
        ccm = self.ui.companyViewCalendar.monthShown()
        ccy = self.ui.companyViewCalendar.yearShown()
        if singleView:
            self.createDetailText(self.currentCompany, ccm,  ccy)
        else:
            for company in mightyController.companylist:
                if self.ui.companyViewList.currentText() == company.name:
                    self.createDetailText(company, ccm, ccy)


    def createDetailText(self, company, ccm,  ccy):
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
                text += "% ("+self.rounder(inMoney)+".-) </li>"
        text += "</ul>"
        if loanSplitSum > 0:
            text += tr("Loansplitsum")+": "+self.rounder(loanSplitSum)+".-/"+str(company.perHours)+tr("h")+"<hr />"
        creditSum = 0
        text += "<h4>"+tr("Credits")+"</h4><ul>"
        for credit in company.credits:
            if (credit.date.month() == ccm and credit.date.year() == ccy) or  self.ui.companyViewCalendarFilter.isChecked() == False:
                creditSum += credit.value
                text += "<li>"+credit.date.toString(dbDateFormat) + ": "+str(credit.value)+""
                if credit.payed:
                    text +=".- "+ tr("is")+" "+tr("payed")+"</li>"
                else:
                    text +=".- "+ tr("is NOT")+" "+tr("payed")+"</li>"
        text += "</ul>"
        if creditSum > 0:
            text += tr("Creditsum")+": "+self.rounder(creditSum)+".- <hr />"
        jobSum = 0
        jobDays = 0
        jobHours = 0
        chargeSum = 0
        text += "<h4>"+tr("Jobs")+"</h4>"
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
                text += "<li>"+job.name+": "+self.rounder(days)+"d * ("+self.rounder(job.hours)+"h /"+str(company.perHours)+" )+" +str(job.correctionHours)+"h = "+self.rounder(hourSpace)+"h * " + str(company.loan)+".-  ="+self.rounder(hourSpace*company.loan)+".- </li>"
                text += "<ul>"
                for charge in job.wcharges:
                    if charge.howManyTimes > 0:
                        chargeSum += charge.value * charge.howManyTimes
                        text += "<li>"+charge.name+": "+str(charge.value)+".- * "+str(charge.howManyTimes)+" times = "+self.rounder(charge.value * days)+".- </li>"
                    else:
                        chargeSum += charge.value * days
                        text += "<li>"+charge.name+": "+str(charge.value)+".- * "+self.rounder(days)+"d = "+self.rounder(chargeSum)+".- </li>"
                text += "</ul>"
        text += "</ul> Sum: "+self.rounder(jobSum)+".- in "+self.rounder(jobHours)+"h / "+self.rounder(jobDays )+" d (+ "+self.rounder(chargeSum)+".- charges) <hr />"
        loanSplitSumDays = loanSplitSum * jobDays
        result = jobSum - loanSplitSumDays - creditSum + chargeSum
        #the end of all results..
        text += "<h4>"+tr("Summary")+"</h4>"
        text += "<ul><li><b>"+self.rounder(jobSum)+".-</b> </li><li><b> - "+self.rounder(loanSplitSumDays)+".-  </b>"+tr("Splits")+"</li><li><b> - "+self.rounder(creditSum)+".- </b>"+tr(  "Credits")+"</li> <li><b> + "+self.rounder(chargeSum)+".- </b> "+tr("Charges")+"</li></ul><hr /> "+tr("Your company should pay")+"<b> "+self.rounder(result)+".- </b>"
        self.ui.companyViewText.setText(text)
                

app = QtGui.QApplication(sys.argv)
lang = ""
for config in mightyController.configlist:
    if config.key == "lang" or config.key == "language":
        if os.path.isfile(config.value):
            lang=config.value
        elif os.path.isfile(config.value+".qm"):
            lang=config.value+".qm"
translator = QtCore.QTranslator()
translator.load(lang,"./")
app.installTranslator(translator)
jobman = Gui()
jobman.show()

sys.exit(app.exec_())
