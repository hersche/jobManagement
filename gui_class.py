from staticTools import *

#the whole gui...
class Gui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        self.roundSum = 0
        # INIT
        self.currentCompany = None
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
        cd = QtCore.QDate.currentDate()
        if singleView == False:
            self.ui.startdate.setDate(cd)
            self.ui.enddate.setDate(cd)
        self.ui.creditDate.setDate(cd)
        self.tabUpdater()
        self.alertBox = QtGui.QMessageBox()
        
        self.ui.mainTab.currentChanged.connect(self.tabUpdater)
        self.ui.viewTabs.currentChanged.connect(self.tabUpdater)
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
    
    def tabUpdater(self,  index=0):
        ci = self.ui.mainTab.currentIndex()
        if ci == 0:
            self.updateCompanyList(True)
        elif ci == 1:
            vci = self.ui.viewTabs.currentIndex()
            if vci == 0:
                self.updateInfoExel()
            elif vci == 1:
                self.updateCompanyViewList()
                self.updateCompanyView()
        elif ci == 2:
            self.updatePersonalChargesList();
            self.updatePersonalCreditList();
        elif ci == 3:
            self.updateConfigList(True)
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
                if item is not None and company.name == item.text():
                    self.currentCompany = company
        if None is not self.currentCompany :
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
                self.ui.baustellenleiter.setText(job.leader)
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

        for spese in self.currentCompany.charges:
            if cm is not None and spese.name == cm.text():
                if spese.save(self.ui.chargesName.text(), self.ui.chargesValue.text()) != -1:
                    self.ui.status.setText(tr("Charge")+" "+self.ui.chargesName.text()+" "+tr("saved"))
                else:
                    sdt.aB(tr("Charge")+" "+tr("could not")+" be "+tr("saved")+". DB-Error. The name maybe exist allready? ")
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
    #--------------------------
    # Showing-Tab
    #--------------------------
    #ugly method, but how else?
    def updateInfoExel(self):
        self.ui.infoExel.clearContents()
        self.ui.infoExel.clear()
        self.sum = 0
        creditStringFinale =""
        creditSumFinale = 0
        if singleView:
            self.ui.infoExel.setHorizontalHeaderLabels((tr( "Jobname"),tr( "Place"), tr( "Leader"), tr( "Loan"),tr( "Time"), tr(  "Charges"), tr( "Splits"), tr( "Summe")))
        else:
            self.ui.infoExel.setHorizontalHeaderLabels((tr( "Companyname"),tr( "Jobname"),tr( "Place"), tr( "Leader"), tr( "Loan"),tr( "Time"), tr(  "Charges"), tr( "Splits"), tr( "Summe")))
        workCalendar = QtCore.QDate.fromString(str(self.ui.workCalendar.monthShown())+"."+str(self.ui.workCalendar.yearShown()),"M.yyyy")
        #proof of concept, have to move..
        rowNr = 0
        sum = 0
        self.roundSum += 1
        infoSearch = self.ui.infoSearch.text()
        infoSearch = infoSearch.lower()
        sdt.updateGraphicView(self.ui,  mightyController.companylist, workCalendar, infoSearch)
        if singleView:
            company = self.currentCompany
            nRowNr, nSum = sdt.filterJobs(self.ui, self.currentCompany, infoSearch,  workCalendar, rowNr, self.sum)
            self.sum += nSum
            self.createCreditTextBox(self.currentCompany, workCalendar)
        else:
            if rowNr==0:
                self.ui.infoExel.insertRow(rowNr)
            for company in mightyController.companylist:
                for job in company.jobs:
                    if cw.insertJobYesNo(self.ui, company, job, infoSearch, workCalendar):
                        sum += sdt.createJobRow(self.ui,  job, company, workCalendar, rowNr, sum) 
                        rowNr +=1
                        self.ui.infoExel.insertRow(rowNr)
                creditString,  creditSum = self.createCreditTextBox(company, workCalendar, sum)
                creditSumFinale += creditSum
                creditStringFinale += creditString
        creditStringFinale+="<hr />Of all companys: "+str(creditSumFinale)+".-"
        self.ui.infoExelCredits.setText(creditStringFinale)
        self.ui.amount.display(sum)


    def createCreditTextBox(self, company, wc, sum):
        creditString =""
        creditSum = 0
        #change to check credit-list-size
        for credit in company.credits:
            if (self.ui.filterCalendar.isChecked() and credit.date.month() == wc.month() and credit.date.year() == wc.year()) or self.ui.filterCalendar.isChecked() == False:
                creditSum += credit.value
                creditString += "-"+credit.name+"/"+credit.date.toString(dbDateFormat)+": "+str(credit.value)+"<br />"
        if creditSum > 0:
            creditString += "------------<br />"+tr("Creditsum")+ "4 :"+company.name+str(creditSum)+"<br />"

        return (creditString,  creditSum)

    def updateCompanyViewList(self):
        if singleView == False:
            self.ui.companyViewList.clear()
            for company in mightyController.companylist:
                self.ui.companyViewList.addItem(company.name)
    def updateCompanyView(self):
        workCalendar = QtCore.QDate.fromString(str(self.ui.companyViewCalendar.monthShown())+"."+str(self.ui.companyViewCalendar.yearShown()),"M.yyyy")
        if singleView:
            self.ui.companyViewText.setText(sdt.createDetailText(self.currentCompany, workCalendar,  self.ui.companyViewCalendarFilter.isChecked()))
        else:
            for company in mightyController.companylist:
                if self.ui.companyViewList.currentText() == company.name:
                    self.ui.companyViewText.setText(sdt.createDetailText(company,workCalendar, self.ui.companyViewCalendarFilter.isChecked()))
#class mathBrain:
#    def __init__(self, companyList):
#        self.hours = 0
#        self.days = 0
#        self.loan = 0
#        for company in companyList:
#            for job in company.jobs:
#                self.days = sdt.calcDaySpace(job.startdate,  job.enddate,  cm,  weekendDays)
#            
#            
#    def calcDays(self):
#        self.days = sdt.calcDaySpace(startdate,  enddate,  cm,  weekendDays)
