import os.path,  sqlite3
from PyQt4 import QtCore
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
    c.execute("CREATE TABLE company (cid  INTEGER PRIMARY KEY, name text UNIQUE, loan REAL, perHours REAL, describtion text)")
    #TODO add weekendDays to job (int) - -1 means no weekend
    c.execute("CREATE TABLE job (jid  INTEGER PRIMARY KEY, name text UNIQUE, place text, comment text, hours real, correctionHours real, weekendDays INTEGER, startdate text, enddate text, leader TEXT, active INTEGER, archived INTEGER, companyid integer)")
    c.execute("CREATE TABLE charges (sid  INTEGER PRIMARY KEY, name text, value real, companyid integer)")
    c.execute("CREATE TABLE credit (crid  INTEGER PRIMARY KEY, name TEXT, value real, date text, payed integer, active integer, companyid integer)")
    c.execute("CREATE TABLE wcharges (wid  INTEGER PRIMARY KEY, jobid INTEGER, chargesid integer, howManyTimes real)")
    # if money is false, the measure is in percent..
    c.execute("CREATE TABLE loanSplit (lsid  INTEGER PRIMARY KEY, name TEXT, value REAL, money INTEGER, companyid INTEGER)")
    c.execute("CREATE TABLE personalFinance (pfid  INTEGER PRIMARY KEY, name TEXT UNIQUE, value REAL, date TEXT,repeat TEXT, timesRepeat INTEGER, plusMinus TEXT, active INTEGER)")
    c.execute("CREATE TABLE config (coid INTEGER PRIMARY KEY,  key TEXT UNIQUE,  value TEXT)")
    
    db.commit()
class Controller:
        def __init__(self):
            self.updateList()
            self.updateConfigList()
        def createCompany(self, name,  loan,  perHours,  describtion):
            try:
                c.execute("INSERT INTO company (name, loan,  perHours, describtion) VALUES (?,?,?,?);",  (name, loan,  perHours, describtion))
                db.commit()
                self.updateList()
            except sqlite3.Error as e:
                if e.args[0] == "column name is not unique":
                    return -2
                print("An DB-error occurred:", e.args[0])
                return -1
        def updateList(self):
            self.companylist = []
            c.execute('select * from company;') 
            for row in c.fetchall():
                self.companylist.append(Company(row[0], row[1], row[2], row[3], row[4]))
        def updatePersonalCreditList(self):
            self.personalCredits = []
            c.execute('select * from credit WHERE companyid = ?',  (str(-1), ))
            for row in c.fetchall():
                self.personalCredits.append(Credit(row[0], row[1], row[2],  row[3],  row[4], row[5], row[6]))
        def updatePersonalChargesList(self):
            self.personalCharges = []
            c.execute('select * from charges WHERE companyid = ?',  (str(-1), ))
            for row in c.fetchall():
                self.personalCharges.append(charges(row[0], row[1], row[2]))
        def createConfig(self, key,  value):
            try:
                c.execute("INSERT INTO config (key, value) VALUES (?,?);",  (key, value))
                db.commit()
                self.updateConfigList()
            except sqlite3.Error as e:
                print("An DB-error occurred:", e.args[0])
                return -1
        def updateConfigList(self):
            self.configlist = []
            c.execute('select * from config;') 
            for row in c.fetchall():
                self.configlist.append(Config(row[0], row[1], row[2]))
        def getCompanyById(self, id):
            for company in self.companylist:
                if company.id == id:
                    return company
        def getCompanyByName(self, name):
            for company in self.companylist:
                if company.name == name:
                    return company
                    
class Config:
    #"CREATE TABLE config (coid INTEGER PRIMARY KEY,  key TEXT,  value TEXT)
    def __init__(self,  id,  key,  value):
        self.id = id
        self.key = key
        self.value = value
        
    def save(self, key,  value):
        try:
            c.execute("UPDATE config SET key=?, value=? WHERE coid=?",  (key, value,  self.id))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
    def delete(self):
        try:
            c.execute("DELETE FROM config WHERE coid=?",  (self.id, ))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
        
                
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
        try:
            c.execute("UPDATE loanSplit SET name=?, value=?, money=? WHERE lsid=?",  (name, float(value), tmpMoney,  self.id))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
            return -1
    def delete(self):
        try:
            c.execute("DELETE FROM loanSplit WHERE lsid=?",  (self.id, ))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
            return -1
    
class charges:
    def __init__(self, id,  name,  value, wchargeid=-1, howManyTimes=-1):
        self.id = id
        self.name = name
        self.value = value
        #just used in workcharges
        self.wchargeId = wchargeid
        self.howManyTimes = howManyTimes
    def save(self, name, value,  howManyTimes=-1):
        try:
            c.execute("UPDATE charges SET name=?, value=? WHERE sid=?",  (name, float(value), self.id))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
            return -1
    def delete(self):
        try:
            c.execute("DELETE FROM charges WHERE sid=?",  (self.id, ))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
            return -1
        
class Credit:
    def __init__(self, id, name,  value,  date, payed, active,  company):
        self.id = id
        self.name = name
        self.value = value
        self.date = QtCore.QDate.fromString(date, dbDateFormat)
        if active == 1:
            self.active = True
        else: 
            self.active = False       
        if payed == 1:
            self.payed = True
        else: 
            self.payed = False
        self.company = company
    def save(self, name,  value,  date,  payed, active,  companyid = -10):
        tmpPayed = 0
        tmpActive = 0
        if payed:
            tmpPayed=1
        if active:
            tmpActive=1
        try:
            c.execute("UPDATE credit SET name=?,value=?, date=?, payed=?,active=? WHERE crid=?",  (name, value, date, tmpPayed, tmpActive, str(self.id)))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
            return -1
    def delete(self):
        try:
            c.execute("DELETE FROM credit WHERE crid=?",  (self.id, ))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
            return -1
        

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
            self.credits.append(Credit(row[0], row[1], row[2],  row[3],  row[4], row[5], row[6]))
    def updateJobList(self):
        self.jobs = []
        c.execute('select * from job WHERE companyid = ?',  (str(self.id), ))
        for row in c.fetchall():
            self.jobs.append(Job(row[0], row[1], row[2], row[3], row[4],  row[5],  row[6],  row[7],  row[8],row[9], row[10],  row[11] , row[12]))
    def updatechargesList(self):
        self.charges = []
        c.execute('select * from charges WHERE companyid = ?',  (str(self.id), ))
        for row in c.fetchall():
            self.charges.append(charges(row[0], row[1], row[2]))
    def createJob(self,  name, place, comment,  hours, correctionHours,  weekendDays,  startdate,  enddate,  leader,  active):
        # (self,  id,  name,  place,  comment,  hours, correctionHours,   startdate,  enddate,  baustellenleiter,  active, companyid):
        try:
            c.execute("INSERT INTO job (name, place, comment,hours, correctionHours, weekendDays, startdate, enddate,  leader, active, companyid) VALUES (?,?,?,?,?,?,?,?,?,?,?)",  (name, place,  comment, hours,correctionHours,  weekendDays,  startdate, enddate,  leader, active,   self.id))
            db.commit()
            self.updateJobList()
        except sqlite3.Error as e:
            if e.args[0] == "column name is not unique":
                return -2
            else:
                print("An DB-error occurred:", e.args[0])
                return -1
            
    def createSpese(self,  name, value, companyid = -10):
        try:
            if companyid != -10:
                c.execute("INSERT INTO charges (name, value, companyid) VALUES (?,?,?)",  ( name, value,  companyid))
            else:
                c.execute("INSERT INTO charges (name, value, companyid) VALUES (?,?,?)",  ( name, value,  self.id))
            db.commit()
            self.updatechargesList()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
            return -1
            
    def createLoanSplit(self, name, value, money):
        if money == True:
            tmpMoney = 1
        else:
            tmpMoney = 0
        try:
            c.execute("INSERT INTO loanSplit (name, value, money, companyid) VALUES (?,?,?,?)",  ( name, value, tmpMoney,  self.id))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
            return -1
        
    def createCredit(self, name,  value, date, payed,  active,  companyid = -10):
        if active:
            tmpActive = 1
        else:
            tmpActive = 0
        if payed:
            tmpPayed = 1
        else:
            tmpPayed = 0
        try:
            if companyid != -10:
                c.execute("INSERT INTO credit (name, value, date, payed,active, companyid) VALUES (?,?,?,?,?,?)",  ( name,  value, date, tmpPayed,tmpActive,  companyid))
            else:
                c.execute("INSERT INTO credit (name, value, date, payed,active, companyid) VALUES (?,?,?,?,?,?)",  ( name,  value, date, tmpPayed,tmpActive,  self.id))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
            return -1
    
    def save(self, name,  loan,  perHours, describtion):
            c.execute("UPDATE company SET name=?, loan=?, perHours=?, describtion=? WHERE cid=?",  (name, loan, perHours, describtion,  self.id))
            db.commit()
    def delete(self):
        try:
            c.execute("DELETE FROM job WHERE companyid=?",  (self.id, ))
            c.execute("DELETE FROM charges WHERE companyid=?",  (self.id, ))
            c.execute("DELETE FROM loanSplit WHERE companyid=?",  (self.id, ))
            c.execute("DELETE FROM company WHERE cid=?",  (self.id, ))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
            return -1
            

class Job:
    def __init__(self,  id,  name,  place,  comment,  hours, correctionHours, weekendDays,  startdate,  enddate,  leader,  active, archived,  companyid):
        self.id = id
        self.name = name
        self.place = place
        self.comment = comment
        self.hours = hours
        self.correctionHours = correctionHours
        self.weekendDays = weekendDays
        self.startdate = QtCore.QDate.fromString(startdate, dbDateFormat)
        self.enddate = QtCore.QDate.fromString(enddate, dbDateFormat)
        self.leader = leader
        self.active = active
        self.archived = False
        if archived == 1:
            self.archived = True
        self.companyid = companyid
        self.updateWchargesList()
    def updateWchargesList(self):
        self.wcharges = []
        c.execute('select * from wcharges WHERE jobid = ?',  (str(self.id), ))
        for co in c.fetchall():
            c.execute('select * from charges WHERE sid = ?',  (str(co[2])))
            for row in c.fetchall():
                self.wcharges.append(charges(row[0], row[1], row[2], co[0], co[3]))
    def addSpese(self,  chargesid, howManyTimes):
        c.execute("INSERT INTO wcharges (jobid, chargesid, howManyTimes) VALUES (?,?,?)",  ( self.id, chargesid, howManyTimes))
        db.commit()
    def removeSpese(self, name,  company):
        for wcharge in self.wcharges:
            if wcharge.name == name:
                try:
                    c.execute("DELETE FROM wcharges WHERE chargesid=?",  (wcharge.wchargeId, ))
                    db.commit()
                except sqlite3.Error as e:
                    print("An DB-error occurred:", e.args[0])
                    return -1
    def saveCharge(self, name,  howManyTimes):
        for wcharge in self.wcharges:
            if wcharge.name == name:
                try:
                    c.execute("UPDATE wcharges SET howManyTimes=? WHERE wid=?",  (howManyTimes,  wcharge.wchargeId))
                    db.commit()
                    self.updateWchargesList()
                except sqlite3.Error as e:
                    print("An DB-error occurred:", e.args[0])
                    return -1
        
    def save(self, name,  place, comment, hours, correctionHours, weekendDays,  startdate, enddate,leader, active, companyid):
            tmpActive = 0
            if active == True:
                tmpActive = 1
            try:
                c.execute("UPDATE job SET name=?, place=?, comment=?, hours=?, correctionHours=?, weekendDays=?, startdate=?, enddate=?, leader=?, active=?, companyid=? WHERE jid=?",  (name, place,  comment, hours, correctionHours, weekendDays,  startdate, enddate, leader, tmpActive, companyid, self.id))
                db.commit()
            except sqlite3.Error as e:
                print("An DB-error occurred:", e.args[0])
                return -1
    def delete(self):
        try:
            c.execute("DELETE FROM wcharges WHERE jobid=?",  (self.id, ))
            c.execute("DELETE FROM job WHERE jid=?",  (self.id, ))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
            return -1
        
