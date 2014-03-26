from lib.models import *
from lib.staticTools import *
singleView = False
singleViewId = -1
mightyController = Controller()
#the whole gui...
class Gui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        logger.debug("|GUI| Init Gui")
        self.roundSum = 0
        # INIT
        
        self.currentCompany = None
        self.showInactive = True
        self.tmpPw = ""
        if mightyController.encryptionObject is not None and mightyController.encryptionObject.name is not "None":
            pw, okCancel = QtGui.QInputDialog.getText(None,tr("Password"),tr("Enter Password"),QtGui.QLineEdit.Password)
            self.tmpPw = pw
            mightyController.encryptionObject.setKey(pw)
        if True is not mightyController.singleView:
            from lib.gui import Ui_MainWindow

        QtGui.QWidget.__init__(self, parent)
        
        if mightyController.singleView:
            self.ui = Ui_MainWindowSingle()
        else:
            self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.updateCompanyList(selectFirst=True)
        if singleView:
            self.onCompanyItemClick("singleView")
        #mightyController.updateCompanyList()
        mightyController.updatePersonalFinancesList()
        cd = QtCore.QDate.currentDate()
        if singleView == False:
            self.ui.startdate.setDate(cd)
            self.ui.enddate.setDate(cd)
        self.ui.creditDate.setDate(cd)
        self.ui.pfDate.setDate(cd)
        self.ui.pfEndDate.setDate(cd)
        self.tabUpdater()
        
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
        self.ui.chargesList.itemClicked.connect(self.onChargeItemClick)
        self.ui.loanDistractionList.itemClicked.connect(self.onLoanDistractionItemClick)
        self.ui.configList.itemClicked.connect(self.onConfigItemClick)
        self.ui.workChargesList.itemClicked.connect(self.onWChargeItemClick)
        self.ui.pfList.itemClicked.connect(self.onPersonalFinanceItemClick)

        #Company-Actions
        if not singleView:
            self.ui.createCompany.clicked.connect(self.onCreateCompany)
            self.ui.deleteCompany.clicked.connect(self.onDeleteCompany)
        self.ui.saveCompany.clicked.connect(self.onSaveCompany)
        self.ui.companyname.returnPressed.connect(self.onSaveCompany)
        
        #Job-Actions
        self.ui.createJob.clicked.connect(self.onCreateJob)
        self.ui.saveJob.clicked.connect(self.onSaveJob)
        self.ui.jobname.returnPressed.connect(self.onSaveJob)
        self.ui.jobplace.returnPressed.connect(self.onSaveJob)
        self.ui.deleteJob.clicked.connect(self.onDeleteJob)
        self.ui.startdate.dateChanged.connect(self.onJobStartDateChanged)
        #self.ui.enddate.dateChanged.connect(self.onJobStartDateChanged)
        #Charge-Actions
        self.ui.createCharge.clicked.connect(self.onCreateCharge)
        self.ui.saveCharge.clicked.connect(self.onSaveCharge)
        self.ui.chargesName.returnPressed.connect(self.onSaveCharge)
        self.ui.deleteCharge.clicked.connect(self.onDeleteCharge)
        self.ui.deleteWorkSpese.clicked.connect(self.onDeleteWorkSpese)
        self.ui.addChargeToJob.clicked.connect(self.onAddWorkSpese)
        self.ui.wChargeSave.clicked.connect(self.onSaveWorkSpese)
        #Credit-Actions
        self.ui.createCredit.clicked.connect(self.onCreateCredit)
        self.ui.saveCredit.clicked.connect(self.onSaveCredit)
        self.ui.deleteCredit.clicked.connect(self.onDeleteCredit)
        
        
        #loanSplit-Actions
        self.ui.createLoanDistraction.clicked.connect(self.onCreateLoanDistraction)
        self.ui.saveLoanDistraction.clicked.connect(self.onSaveLoanDistraction)
        self.ui.deleteLoanDistraction.clicked.connect(self.onDeleteLoanDistraction)
        
        #config-Actions
        self.ui.createConfig.clicked.connect(self.onCreateConfig)
        self.ui.saveConfig.clicked.connect(self.onSaveConfig)
        self.ui.deleteConfig.clicked.connect(self.onDeleteConfig)
        #---------------------
        #personal tab
        #--------------------- 
        #Charge-Actions
        
        self.ui.pfCreate.clicked.connect(self.onCreatePersonalFinance)
        self.ui.pfSave.clicked.connect(self.onSavePersonalFinance)
        self.ui.pfDelete.clicked.connect(self.onDeletePersonalFinance)
        self.ui.pfDate.dateChanged.connect(self.onPfStartDateChanged)

        self.ui.pfCalendar.currentPageChanged.connect(self.updatePersonalFinanceText)
        self.ui.pfCalendarEnabled.clicked.connect(self.updatePersonalFinanceText)
        self.ui.pfSearchEnabled.clicked.connect(self.updatePersonalFinanceText)
        self.ui.pfSearch.textChanged.connect(self.updatePersonalFinanceText)
        
        
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
            self.ui.companyViewSelect.currentIndexChanged.connect(self.updateCompanyView)
        self.ui.companyViewCalendar.currentPageChanged.connect(self.updateCompanyView)
        self.ui.companyViewCalendarFilter.clicked.connect(self.updateCompanyView)
    
    def tabUpdater(self,  index=0):
        try: 
            ci = self.ui.mainTab.currentIndex()
            #if ci == 0:
                #self.updateCompanyList(selectFirst=True)
                #self.updateJobList(selectFirst=True)
            if ci == 1:
                vci = self.ui.viewTabs.currentIndex()
                if vci == 0:
                    self.updateInfoExel()
                elif vci == 1:
                    self.updateCompanyViewSelect()
                    self.updateCompanyView()
            elif ci == 2:
                self.updatePersonalFinancesList()
                #self.updatePersonalCreditList();
            elif ci == 3:
                self.updateConfigList(True)
        except Exception as e:
            print(e)
    #----------------------
    # Updaters
    #-----------------------
    def updateCompanyList(self, selectFirst=False,name=""):
        if mightyController.singleView == False:
            if mightyController.encryptionObject is not None:
                mightyController.encryptionObject.setKey(self.tmpPw)
            mightyController.updateCompanyList()
            self.ui.companyList.clear()
            i=0
            for company in mightyController.companylist:
                self.ui.companyList.addItem(company.name)
                if name == company.name:
                    self.ui.companyList.setCurrentRow(i)
                    self.onCompanyItemClick(self.ui.companyList.currentItem())
                i+=1
            if selectFirst and len(mightyController.companylist) > 0:
                self.ui.companyList.setCurrentRow(0)
                self.onCompanyItemClick(self.ui.companyList.currentItem())
    def updateJobList(self, selectFirst=False,  name=""):
        self.ui.jobList.clear()
        if mightyController.encryptionObject is not None:
            mightyController.encryptionObject.setKey(self.tmpPw)
        self.currentCompany.updateJobList()
        i=0
        for job in self.currentCompany.jobs:
            if (self.showInactive == True) or (job.active == 1):
                self.ui.jobList.addItem(job.name)
                if job.name == name:
                  self.ui.jobList.setCurrentRow(i)
                  self.onJobItemClick(self.ui.jobList.currentItem())
                i+=1
        if selectFirst:
            self.ui.jobList.setCurrentRow(0)
            self.onJobItemClick(self.ui.jobList.currentItem())
    def updateChargesList(self,selectFirst=False,name=""):
        self.ui.chargesList.clear()
        if mightyController.encryptionObject is not None:
            mightyController.encryptionObject.setKey(self.tmpPw)
        self.currentCompany.updateChargesList()
        i=0
        for charge in self.currentCompany.charges:
            self.ui.chargesList.addItem(charge.name)
            if name==charge.name:
                self.ui.chargesList.setCurrentRow(i)
                self.onChargeItemClick(self.ui.chargesList.currentItem())
            i+=1
        if selectFirst:
            self.ui.chargesList.setCurrentRow(0)
            self.onChargeItemClick(self.ui.chargesList.currentItem())
    def updatePersonalFinancesList(self,  selectFirst=False,  name=""):
        self.ui.pfList.clear()
        if mightyController.encryptionObject is not None:
            mightyController.encryptionObject.setKey(self.tmpPw)
        mightyController.updatePersonalFinancesList()
        self.updatePersonalFinanceText()
        i=0
        for pf in mightyController.personalFinances:
            self.ui.pfList.addItem(pf.name)
            if name==pf.name:
                self.ui.pfList.setCurrentRow(i)
                self.onPersonalFinanceItemClick(self.ui.pfList.currentItem())
            i+=1
        if selectFirst:
            self.ui.pfList.setCurrentRow(0)
            self.onPersonalFinanceItemClick(self.ui.pfList.currentItem())
    def updateLoanDistractionList(self,  selectFirst=False,  name=""):
        self.ui.loanDistractionList.clear()
        if mightyController.encryptionObject is not None:
            mightyController.encryptionObject.setKey(self.tmpPw)
        self.currentCompany.updateLoanDistractionList()
        for loanDistraction in self.currentCompany.loanDistractions:
            self.ui.loanDistractionList.addItem(loanDistraction.name)
        if selectFirst:
            self.ui.loanDistractionList.setCurrentRow(0)
            self.onLoanDistractionItemClick(self.ui.loanDistractionList.currentItem())
    def updateConfigList(self,selectFirst=False,name=""):
        self.ui.configList.clear()
        mightyController.updateConfigList()
        i=0
        for config in mightyController.configlist:
            self.ui.configList.addItem(config.key)
            if config.key == name:
                self.ui.configList.setCurrentRow(i)
                self.onConfigItemClick(self.ui.configList.currentItem())
            i+=1
        if selectFirst:
            self.ui.configList.setCurrentRow(0)
            self.onConfigItemClick(self.ui.configList.currentItem())
            
    def updateCreditList(self,  selectFirst=False, valueDate=""):
        self.ui.creditList.clear()
        if mightyController.encryptionObject is not None:
            mightyController.encryptionObject.setKey(self.tmpPw)
        self.currentCompany.updateCreditList()
        for credit in self.currentCompany.credits:
            self.ui.creditList.addItem(credit.name+" / "+str(credit.value) +".- "+credit.date.toString(dbDateFormat))
        if selectFirst:
            self.ui.creditList.setCurrentRow(0)
            self.onCreditItemClick(self.ui.creditList.currentItem())
    def updateWorkchargesList(self,  selectFirst=False,  name=""):
        self.ui.workChargesList.clear()
        if mightyController.encryptionObject is not None:
            mightyController.encryptionObject.setKey(self.tmpPw)
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
    
    def onJobStartDateChanged(self):
        self.ui.enddate.setMinimumDate(self.ui.startdate.date())
        logger.debug("Refreshed minimum Enddate")
        
    def onPfStartDateChanged(self):
        self.ui.pfEndDate.setMinimumDate(self.ui.pfDate.date())
    
    def onCompanyItemClick(self,  item):
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
            self.updateChargesList(True)
            self.updateCreditList(True)
            self.updateLoanDistractionList(True)
    def onChargeItemClick(self, item):
        for charge in self.currentCompany.charges:
            if charge.name == item.text():
                self.ui.chargesName.setText(charge.name)
                self.ui.chargesValue.setValue(charge.value)
    def onPersonalFinanceItemClick(self, item):
        for pf in mightyController.personalFinances:
            if pf.name == item.text():
                self.ui.pfName.setText(pf.name)
                self.ui.pfValue.setValue(pf.value)
                self.ui.pfDate.setDate(pf.date)
                self.ui.pfEndDate.setDate(pf.endDate)
                self.ui.pfRepeatTimes.setValue(pf.timesRepeat)
                if pf.plusMinus == "+":
                    self.ui.pfPlusMinus.setCurrentIndex(0)
                else:
                    self.ui.pfPlusMinus.setCurrentIndex(1)
                if pf.repeat == tr("None"):
                    self.ui.pfRepeat.setCurrentIndex(0)
                elif pf.repeat == tr("Daily"):
                    self.ui.pfRepeat.setCurrentIndex(1)
                elif pf.repeat == tr("Weekly"):
                    self.ui.pfRepeat.setCurrentIndex(2)
                else:
                    self.ui.pfRepeat.setCurrentIndex(3)
                self.ui.pfActive.setChecked(pf.active)
    def onWChargeItemClick(self, item):
        jobSelect = self.ui.jobList.currentItem()
        for  job in self.currentCompany.jobs:
            if job.name == jobSelect.text():
                for charge in job.wcharges:
                    if charge.name == item.text():
                        self.ui.wChargeTimes.setValue(charge.howManyTimes)
    def onLoanDistractionItemClick(self, item):
        for loanDistraction in self.currentCompany.loanDistractions:
            if loanDistraction.name == item.text():
                self.ui.loanDistractionName.setText(loanDistraction.name)
                self.ui.loanDistractionValue.setValue(loanDistraction.value)
                self.ui.loanDistractionMoney.setChecked(loanDistraction.money)
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
                    self.ui.enddate.setMinimumDate(job.startdate)
                    self.ui.enddate.setDate(job.enddate)
                    self.ui.daysCalc.setText(str(job.startdate.daysTo(job.enddate)+1)+ " "+ tr("days"))
                    self.ui.hoursCalc.setText(str((job.startdate.daysTo(job.enddate)+1)*job.hours)+" "+ tr(" hours"))
                self.updateWorkchargesList()
                if job.active == 1:
                    self.ui.active.setChecked(True)
                else:
                    self.ui.active.setChecked(False)
                    
    #-------------
    # personal Finance-Actions
    #--------------
    def onCreatePersonalFinance(self):
        #self.currentCompany.createCharge(self.ui.chargesName.text(), self.ui.chargesValue.text())
        mightyController.createPersonalFinance(self.ui.pfName.text(), self.ui.pfValue.text(), self.ui.pfDate.text(),self.ui.pfEndDate.text(), self.ui.pfRepeat.currentText(), self.ui.pfRepeatTimes.value(), self.ui.pfPlusMinus.currentText(), self.ui.pfActive.isChecked(), encrypted)
        # @TODO select the created!
        self.updatePersonalFinancesList(False,self.ui.pfName.text())
    def onSavePersonalFinance(self):
        cm = self.ui.pfList.currentItem()
        for pf in mightyController.personalFinances:
            if cm is not None and pf.name == cm.text():
                if pf.save(self.ui.pfName.text(), self.ui.pfValue.text(), self.ui.pfDate.text(),self.ui.pfEndDate.text(), self.ui.pfRepeat.currentText(), self.ui.pfRepeatTimes.value(), self.ui.pfPlusMinus.currentText(), self.ui.pfActive.isChecked()) != -1:
                    self.ui.status.setText(tr("Personal Finance")+" "+self.ui.pfName.text()+" "+tr("saved"))
                else:
                    logger.error(tr("Personal Finance")+" "+tr("could not")+" be "+tr("saved")+". DB-Error. The name maybe exist allready?")
                    sdt.aB(tr("Personal Finance")+" "+tr("could not")+" be "+tr("saved")+". DB-Error. The name maybe exist allready?")
        self.updatePersonalFinancesList(False,self.ui.pfName.text())
    def onDeletePersonalFinance(self):
        cm = self.ui.pfList.currentItem()
        success = False
        for pf in mightyController.personalFinances:
            if cm is not None and pf.name == cm.text():
                pf.delete()
                success = True
                self.ui.status.setText(tr("Charge")+" "+cm.text()+" "+tr("deleted"))
        if not success:
            logger.error(tr("Charge")+" "+tr("could not")+" be "+tr("deleted"))
            sdt.aB(tr("Charge")+" "+tr("could not")+" be "+tr("deleted"))
            
        else:
            self.updatePersonalFinancesList(True)
    def updatePersonalFinanceText(self):
        self.ui.pfSummary.clear()
        self.ui.pfSummary.setText(sdt.createPersonalFinancesHtml(mightyController.personalFinances,  self.ui))
            
    #-------------
    # Charges-Actions
    #--------------
    def onCreateCharge(self):
        self.currentCompany.createCharge(self.ui.chargesName.text(), self.ui.chargesValue.text())
        # @TODO select the created!
        self.updateChargesList(False,self.ui.chargesName.text())
    def onSaveCharge(self):
        cr = self.ui.chargesList.currentRow()
        cm = self.ui.chargesList.currentItem()

        for charge in self.currentCompany.charges:
            if cm is not None and charge.name == cm.text():
                if charge.save(self.ui.chargesName.text(), self.ui.chargesValue.text()) != -1:
                    self.ui.status.setText(tr("Charge")+" "+self.ui.chargesName.text()+" "+tr("saved"))
                else:
                    logger.error(tr("Charge")+" "+tr("could not")+" be "+tr("saved")+". DB-Error. The name maybe exist allready?")
                    sdt.aB(tr("Charge")+" "+tr("could not")+" be "+tr("saved")+". DB-Error. The name maybe exist allready?")
        else:
            self.updateChargesList(True)
            self.updateWorkchargesList(True)
            self.ui.chargesList.setCurrentRow(cr)
            self.ui.chargesList.setCurrentItem(cm)
    def onDeleteCharge(self):
        cm = self.ui.chargesList.currentItem()
        success = False
        for charge in self.currentCompany.charges:
            if cm is not None and charge.name == cm.text():
                charge.delete()
                success = True
                self.ui.status.setText(tr("Charge")+" "+cm.text()+" "+tr("deleted"))
        if not success:
            logger.error(tr("Charge")+" "+tr("could not")+" be "+tr("deleted"))
            sdt.aB(tr("Charge")+" "+tr("could not")+" be "+tr("deleted"))
        else:
            self.updateChargesList(True)
    #-------------
    # loanDistraction-Actions
    #--------------
    def onCreateLoanDistraction(self):
        self.currentCompany.createLoanDistraction(self.ui.loanDistractionName.text(), self.ui.loanDistractionValue.text(),  self.ui.loanDistractionMoney.isChecked())
        # @TODO select the created!
        self.ui.status.setText(tr("LoanDistraction")+" "+self.ui.loanDistractionName.text()+" "+tr("created"))
        self.updateLoanDistractionList(True)
    def onSaveLoanDistraction(self):
        cr = self.ui.loanDistractionList.currentRow()
        cm = self.ui.loanDistractionList.currentItem()
        success = False
        for loanDistraction in self.currentCompany.loanDistractions:
            if cm is not None and loanDistraction.name == cm.text():
                loanDistraction.save(self.ui.loanDistractionName.text(), self.ui.loanDistractionValue.text(),  self.ui.loanDistractionMoney.isChecked())
                success = True
                self.ui.status.setText(tr("LoanSplit")+" "+self.ui.loanSplitName.text()+" "+tr("saved"))
        if not success:
            logger.error(tr("LoanSplit")+" "+tr("could not")+" be "+tr("saved"))
            sdt.aB(tr("LoanSplit")+" "+tr("could not")+" be "+tr("saved"))
            
        else:
            self.updateLoanDistractionList()
            self.ui.loanDistractionList.setCurrentRow(cr)
            self.ui.loanDistractionList.setCurrentItem(cm)
    def onDeleteLoanDistraction(self):
        cm = self.ui.loanDistractionList.currentItem()
        success = False
        for loanDistraction in self.currentCompany.loanDistractions:
            if cm is not None and loanDistraction.name == cm.text():
                loanDistraction.delete()
                success = True
                self.ui.status.setText(tr("LoanSplit")+" "+cm.text()+" "+tr("deleted"))
        if not success:
            logger.error(tr("Charge")+" "+tr("could not")+" be "+tr("saved"))
            sdt.aB(tr("Charge")+" "+tr("could not")+" be "+tr("saved"))
        else:
            self.updateLoanDistractionList(True)
        
    #-------------
    # config-Actions
    #--------------
    def onCreateConfig(self):
        mightyController.createConfig(self.ui.configKey.text(), self.ui.configValue.text())
        # @TODO select the created!
        self.ui.status.setText(tr("Config")+" "+self.ui.configKey.text()+" "+tr("created"))
        if self.ui.configKey.text() == "encrypted" and self.ui.configValue.text() != "None":
            pw, okCancel = QtGui.QInputDialog.getText(None,tr("Password"),tr("Enter Password"),QtGui.QLineEdit.Password)
            self.tmpPw = pw
            newCryptManager = cm(scm.getMod(self.ui.configValue.text()), pw)
            mightyController.updateEos(newCryptManager)
            scm.migrateEncryptionData(newCryptManager, mightyController)
        self.updateConfigList(False,self.ui.configKey.text())
        
    def onSaveConfig(self):
        cI = self.ui.configList.currentItem()
        ciText = cI.text()
        for config in mightyController.configlist:
            if cI is not None and config.key == ciText:
                config.save(self.ui.configKey.text(), self.ui.configValue.text())
                self.ui.status.setText(tr("Config")+" "+self.ui.configKey.text()+" "+tr("saved"))
                if self.ui.configKey.text() == "encrypted":
                    if self.ui.configValue.text() != "None":
                      logger.error("not none but "+self.ui.configValue.text())
                      pw, okCancel = QtGui.QInputDialog.getText(None,tr("Password"),tr("Enter Password"),QtGui.QLineEdit.Password)
                      self.tmpPw = pw
                      nCm = cm(scm.getMod(self.ui.configValue.text()), pw)
                    else:
                      nCm = None
                    scm.migrateEncryptionData(nCm, mightyController)
                    mightyController.encryptionObject = nCm
                    mightyController.updateEos(nCm)
        self.updateConfigList(False,self.ui.configKey.text())
    def onDeleteConfig(self):
        cm = self.ui.configList.currentItem()
        success = False
        for config in mightyController.configlist:
            if cm is not None and config.key == cm.text():
                config.delete()
                success = True
                self.ui.status.setText(tr("Charge")+" "+cm.text()+" "+tr("deleted"))
        if not success:
            logger.error(tr("Charge")+" "+tr("could not")+" be "+tr("saved"))
            sdt.aB(tr("Charge")+" "+tr("could not")+" be "+tr("saved"))
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
            logger.error(tr("Credit")+" "+tr("could not")+" be "+tr("saved"))
            sdt.aB(tr("Credit")+" "+tr("could not")+" be "+tr("saved"))
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
            logger.error(tr("Credit")+" "+tr("could not")+" be "+tr("deleted"))
            sdt.aB(tr("Credit")+" "+tr("could not")+" be "+tr("deleted"))
        else:
            self.updateCreditList(True)
        

    #--------------------
    # Company-Actions
    #---------------------
    def onCreateCompany(self):
        b = mightyController.createCompany(self.ui.companyname.text(),  self.ui.loan.text(),  self.ui.perHours.text(),  self.ui.companydescription.toPlainText()) 
        if b== -2:
            logger.error(tr("Company already exist, please choose another name"))
            sdt.aB(tr("Company already exist, please choose another name"))
        elif b == -1:
            logger.error(tr("A DB-Failure is happent. Please check the console."))
            sdt.aB(tr("A DB-Failure is happent. Please check the console."))
        else:
            self.updateCompanyList(False,self.ui.companyname.text())
    def onSaveCompany(self):
        if self.currentCompany is not None:
            if singleView:
                self.currentCompany.save(self.ui.companyname.text(),  self.ui.loan.text(), 1, "SingleViewCompany")
            else:
                self.currentCompany.save(self.ui.companyname.text(),  self.ui.loan.text(), self.ui.perHours.text(), self.ui.companydescription.toPlainText())
        else:
            sdt.aB("Company could not be saved")
        self.updateCompanyList(False,self.ui.companyname.text())
    def onDeleteCompany(self):
        if self.currentCompany is not None:
            self.currentCompany.delete()
        else:
            sdt.aB("Company could not be deleted")
        self.updateCompanyList(True)
        
        
    #------------------------
    # Job-Actions
    #------------------------
    def onCreateJob(self):
        tmpCheck = 0
        if self.ui.active.isChecked():
            tmpCheck = 1
        if singleView:
            b = self.currentCompany.createJob(self.ui.jobname.text(), self.ui.jobplace.text(), self.ui.jobComment.toPlainText(), self.ui.hours.text(),self.ui.correctionHours.text(),  self.ui.weekendDays.value(),  -1,  -1,  self.ui.baustellenleiter.text(),  tmpCheck)
        else:
            b = self.currentCompany.createJob(self.ui.jobname.text(), self.ui.jobplace.text(), self.ui.jobComment.toPlainText(), self.ui.hours.text(),self.ui.correctionHours.text(),  self.ui.weekendDays.value(),  self.ui.startdate.text(),  self.ui.enddate.text(),  self.ui.baustellenleiter.text(),  tmpCheck)
        # @TODO select the created!!
        if b== -2:
            sdt.aB(tr("Job already exist, please choose another name"))
        elif b == -1:
            sdt.aB(tr("A DB-Failure is happent. Please check the console."))
        else:
            self.updateJobList(False,self.ui.jobname.text())
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
        self.updateJobList(False,job.name)
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
        self.ui.infoExel.insertRow(0)
        if singleView:
            company = self.currentCompany
            for job in company.jobs:
                if cw.insertJobYesNo(self.ui, company, job, infoSearch, workCalendar):
                    sum += sdt.createJobRow(self.ui,  job, company, workCalendar, rowNr, sum) 
                    rowNr +=1
                    self.ui.infoExel.insertRow(rowNr)
            creditString, creditSumFinale = sdt.createCreditTextBox(self.currentCompany, self.ui)
        else:
            for company in mightyController.companylist:
                sl = sorted(company.jobs, key=lambda job: job.startdate,  reverse=True)
                for job in sl:
                    if cw.insertJobYesNo(self.ui, company, job, infoSearch, workCalendar):
                        sum += sdt.createJobRow(self.ui,  job, company, workCalendar, rowNr, sum) 
                        rowNr +=1
                        self.ui.infoExel.insertRow(rowNr)
                creditString,  creditSum = sdt.createCreditTextBox(company, self.ui)
                creditSumFinale += creditSum
                creditStringFinale += creditString
        creditStringFinale+="<hr />Of all companys: "+str(creditSumFinale)+".-"
        self.ui.infoExelCredits.setText(creditStringFinale)
        self.ui.amount.display(sum-creditSumFinale)

    def updateCompanyViewSelect(self):
        if singleView == False:
            self.ui.companyViewSelect.clear()
            for company in mightyController.companylist:
                self.ui.companyViewSelect.addItem(company.name)
    def updateCompanyView(self):
        workCalendar = QtCore.QDate.fromString(str(self.ui.companyViewCalendar.monthShown())+"."+str(self.ui.companyViewCalendar.yearShown()),"M.yyyy")
        if singleView:
            self.ui.companyViewText.setText(sdt.createDetailText(self.currentCompany, workCalendar,  self.ui.companyViewCalendarFilter.isChecked()))
        else:
            for company in mightyController.companylist:
                if self.ui.companyViewSelect.currentText() == company.name:
                    self.ui.companyViewText.setText(sdt.createDetailText(company,workCalendar, self.ui.companyViewCalendarFilter.isChecked()))
