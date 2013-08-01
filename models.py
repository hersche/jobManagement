import os.path,  sqlite3
from PyQt4 import QtCore,  QtGui
from header import *
#from Crypto.Cipher import * 
fileExist = True
singleView = False
encrypted = ""
#...dann wird das überprüft..
if os.path.isfile('jobmanagement.db') == False:
    #..und ggf umgestellt..
    fileExist = False
#..denn sqlite3.connect erstellt immer ein file!
db = sqlite3.connect('jobmanagement.db')
#aber wir brauchen ja den cursor, um die db initialisieren zu können.
c = db.cursor()
if fileExist == False:
    c.execute("CREATE TABLE company (cid  INTEGER PRIMARY KEY, name text UNIQUE, loan text, perHours REAL, describtion text, encrypted text)")
    #TODO add weekendDays to job (int) - -1 means no weekend
    c.execute("CREATE TABLE job (jid  INTEGER PRIMARY KEY, name text UNIQUE, place text, comment text, hours text, correctionHours text, weekendDays INTEGER, startdate text, enddate text, leader TEXT, active text, archived text, companyid text, encrypted text)")
    c.execute("CREATE TABLE charges (sid  INTEGER PRIMARY KEY, name text, value text, companyid text, encrypted text)")
    c.execute("CREATE TABLE credit (crid  INTEGER PRIMARY KEY, name TEXT, value text, date text, payed text, active text, companyid text, encrypted text)")
    c.execute("CREATE TABLE wcharges (wid  INTEGER PRIMARY KEY, jobid text, chargesid text, howManyTimes text, encrypted text)")
    # if money is false, the measure is in percent..
    c.execute("CREATE TABLE loanSplit (lsid  INTEGER PRIMARY KEY, name TEXT, value text, money text, companyid text, encrypted text)")
    c.execute("CREATE TABLE personalFinance (pfid  INTEGER PRIMARY KEY, name TEXT UNIQUE, value text, date TEXT,repeat TEXT, timesRepeat text, plusMinus TEXT, active text, encrypted text)")
    c.execute("CREATE TABLE config (coid INTEGER PRIMARY KEY,  key TEXT UNIQUE,  value TEXT, encrypted text)")
    
    db.commit()
    

class Controller:
        def __init__(self):
            self.eo = None
            self.encryption = ""
            self.lang = ""
            self.singleView = False
            self.singleViewId = -1
            self.updateConfigList()

        def createCompany(self, name,  loan,  perHours,  describtion):
            try:
                if self.eo != None:
                    c.execute("INSERT INTO company (name, loan,  perHours, describtion, encrypted) VALUES (?,?,?,?,?);",  (self.eo.encrypt(name), self.eo.encrypt(loan),  self.eo.encrypt(perHours), self.eo.encrypt(describtion), encrypted))
                else:
                    c.execute("INSERT INTO company (name, loan,  perHours, describtion, encrypted) VALUES (?,?,?,?,?);",  (name, loan,  perHours, describtion, encrypted))
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
                if self.eo != None:
                    self.companylist.append(Company(row[0], self.eo.decrypt(row[1]), self.eo.decrypt(row[2]), self.eo.decrypt(row[3]), self.eo.decrypt(row[4]),row[5],  self.eo))
                else:
                    self.companylist.append(Company(row[0], row[1], row[2], row[3], row[4],row[5],  self.eo))
        def updatePersonalFinancesList(self):
            self.personalFinances = []
            try:
                c.execute('select * from personalFinance')
                for row in c.fetchall():
                    if self.eo != None:
                        self.personalFinances.append(personalFinance(row[0], self.eo.decrypt(row[1]), self.eo.decrypt(row[2]), self.eo.decrypt(row[3]), self.eo.decrypt(row[4]), self.eo.decrypt(row[5]), self.eo.decrypt(row[6]), self.eo.decrypt(row[7]), row[8], self.eo))
                    else:
                        self.personalFinances.append(personalFinance(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], self.eo))
            except sqlite3.Error as e:
                print("An DB-error occurred:", e.args[0])
                return -1
        def createPersonalFinance(self, name,  value, date, repeat, timesRepeat, plusMinus,  active,  encrypted ):
            try:
                if self.eo != None:
                    c.execute("INSERT INTO personalFinance (name,  value, date, repeat, timesRepeat, plusMinus,  active,  encrypted) VALUES (?,?,?,?,?,?,?,?);",  (self.eo.encrypt(name),  self.eo.encrypt(value), self.eo.encrypt(date), self.eo.encrypt(repeat), self.eo.encrypt(timesRepeat), self.eo.encrypt(plusMinus),  self.eo.encrypt(active),  encrypted))
                else:
                    c.execute("INSERT INTO personalFinance (name,  value, date, repeat, timesRepeat, plusMinus,  active,  encrypted) VALUES (?,?,?,?,?,?,?,?);",  (name,  value, date, repeat, timesRepeat, plusMinus,  active,  encrypted))
                db.commit()
                self.updateConfigList()
            except sqlite3.Error as e:
                print("An DB-error occurred:", e.args[0])
                return -1
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
            for config in self.configlist:
                if (config.key.lower() == "single" or config.key.lower() == "singleview") and (config.value.lower() == "true" or config.value.lower() == "1"):
                    self.singleView = True
                    from gui_single import Ui_MainWindowSingle
                #elif config.key.lower()== "singleviewcname":
                    #singleViewName = config.value
                elif config.key.lower()== "encrypted":
                    
                    self.encryption = config.value
                    
                elif config.key.lower()== "singleviewcid":
                    singleViewId = config.value
                elif config.key == "lang" or config.key == "language":
                    if os.path.isfile(config.value):
                        self.lang=config.value
                    elif os.path.isfile(config.value+".qm"):
                        self.lang=config.value+".qm"
        def getCompanyById(self, id):
            for company in self.companylist:
                if company.id == id:
                    return company
        def getCompanyByName(self, name):
            for company in self.companylist:
                if company.name == name:
                    return company
              
           
        
     
      #CREATE TABLE personalFinance (pfid  INTEGER PRIMARY KEY, name TEXT UNIQUE, value REAL, date TEXT,repeat TEXT, timesRepeat INTEGER, plusMinus TEXT, active INTEGER, encrypted integer)")   
class personalFinance:
    def __init__(self, id, name, value, date, repeat, timesRepeat, plusMinus,  active,  encrypted, eo):
        self.id = id
        self.name = name
        self.value = float(value)
        self.date=QtCore.QDate.fromString(date, dbDateFormat)
        self.repeat =repeat
        self.timesRepeat = int(timesRepeat)
        self.plusMinus=plusMinus
        tmpActive = False
        if active == "1":
            tmpActive = True
        self.active = tmpActive
        self.encrypted = encrypted
        self.eo = eo
    def save(self, name, value, date, repeat, timesRepeat, plusMinus, active):
        try:
            if self.eo != None:
                c.execute("UPDATE personalFinance SET name=?,value=?,date=?,repeat=?,timesRepeat=?,plusMinus=?,active=?,encrypted=? WHERE pfid=?",  (self.eo.encrypt(name), self.eo.encrypt(value), self.eo.encrypt(date), self.eo.encrypt(repeat), self.eo.encrypt(timesRepeat), self.eo.encrypt(plusMinus), self.eo.encrypt(active), self.encrypted,self.id))
            else:
                c.execute("UPDATE personalFinance SET name=?,value=?,date=?,repeat=?,timesRepeat=?,plusMinus=?,active=?,encrypted=? WHERE pfid=?",  (name, value, date, repeat, timesRepeat, plusMinus, active, self.encrypted,self.id))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
    def delete(self):
        try:
            c.execute("DELETE FROM personalFinance WHERE pfid=?",  (self.id, ))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
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
    def __init__(self, id,  name, value,  money, encrypted, eo):
        self.id = id
        self.name = name
        self.value = float(value)
        self.encrypted = encrypted
        self.eo = eo
        if money == "1":
            #The value is calcucalted as money (.-)
            self.money = True
        else:
            #The value is calculated as percent (%)
            self.money = False
    def save(self, name,  value,  money):
        tmpMoney = "0"
        if money==True:
            tmpMoney = "1"
        try:
            if self.eo != None:
                c.execute("UPDATE loanSplit SET name=?, value=?, money=? WHERE lsid=?",  (self.eo.encrypt(name), self.eo.encrypt(value), self.eo.encrypt(tmpMoney),  self.id))
            else:
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
#sid  INTEGER PRIMARY KEY, name text, value text, companyid text, encrypted text)")
class charges:
    def __init__(self, id,  name,  value, wchargeid=-1, howManyTimes=-1, encrypted="", eo=None):
        self.id = id
        self.name = name
        self.value = float(value)
        self.encrypted = encrypted
        self.eo = eo
        #just used in workcharges
        self.wchargeId = int(wchargeid)
        self.encrypted = encrypted
        self.howManyTimes = int(howManyTimes)
    def save(self, name, value,  howManyTimes=-1):
        try:
            if self.eo != None:
                c.execute("UPDATE charges SET name=?, value=? WHERE sid=?",  (self.eo.encrypt(name), self.eo.encrypt(value), self.id))
            else:
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
    def __init__(self, id, name,  value,  date, payed, active,  company, encrypted, eo):
        self.id = id
        self.name = name
        self.value = float(value)
        self.date = QtCore.QDate.fromString(date, dbDateFormat)
        self.encrypted = encrypted
        self.eo = eo
        if active == "1":
            self.active = True
        else: 
            self.active = False       
        if payed == "1":
            self.payed = True
        else: 
            self.payed = False
        self.company = company
    def save(self, name,  value,  date,  payed, active,  companyid = -10):
        tmpPayed = "0"
        tmpActive = "0"
        if payed:
            tmpPayed="1"
        if active:
            tmpActive="1"
        try:
            if self.eo != None:
                c.execute("UPDATE credit SET name=?,value=?, date=?, payed=?,active=? WHERE crid=?",  (self.eo.encrypt(name, self.eo.encrypt(value), self.eo.encrypt(date), self.eo.encrypt(tmpPayed), self.eo.encrypt(tmpActive), str(self.id))))
            else:
                c.execute("UPDATE credit SET name=?,value=?, date=?, payed=?,active=? WHERE crid=?",  (name, value, date, tmpPayed, tmpActive, str(self.id)))
            db.commit()
        except sqlite3.Error as e:
            print("credit save An DB-error occurred:", e.args[0])
            return -1
    def delete(self):
        try:
            c.execute("DELETE FROM credit WHERE crid=?",  (self.id, ))
            db.commit()
        except sqlite3.Error as e:
            print("An DB-error occurred:", e.args[0])
            return -1
        

class Company:
    def __init__(self, id,  name,  loan, perHours,  describtion,encrypted,  eo):
        self.id = id
        self.name = name
        self.eo = eo
        self.encrypted = encrypted
        self.loan = float(loan)
        self.perHours = float(perHours)
        self.describtion = describtion
        self.updateJobList()
        self.updatechargesList()
        self.updateCreditList()
        self.updateLoanSplitList()

        

    def updateLoanSplitList(self):
        self.loanSplits = []
        if self.eo != None:
            sString = "select * from loanSplit WHERE lsid = ?"
            c.execute('select lsid, companyid from loanSplit')
            for r in c.fetchall():
                if self.eo.decrypt(r[1]) == str(self.id):
                    c.execute(sString,  (str(r[0]), ))
                    for row in c.fetchall():
                        self.loanSplits.append(loanSplit(row[0], self.eo.decrypt(row[1]),self.eo.decrypt(row[2]),self.eo.decrypt(row[3]), row[4], self.eo))
        else:
            for row in c.fetchall():
                c.execute("SELECT * FROM loanSplit WHERE companyid = ?", (str(self.id), ))
                self.loanSplits.append(loanSplit(row[0], row[1],row[2],row[3], row[4], self.eo))
    def updateCreditList(self):
        self.credits = []
        if self.eo != None:
            sString = "select * from credit WHERE crid=?"
            c.execute('select crid, companyid from credit')
            for r in c.fetchall():
                if self.eo.decrypt(r[1]) == str(self.id):
                    print(str(r[0]))
                    c.execute(sString,  (str(r[0]), ))
                    for row in c.fetchall():
                        self.credits.append(Credit(row[0], self.eo.decrypt(row[1]), self.eo.decrypt(row[2]),  self.eo.decrypt(row[3]),  self.eo.decrypt(row[4]), self.eo.decrypt(row[5]), self.eo.decrypt(row[6]), row[7],self.eo))
        else:
            c.execute('select * from credit WHERE companyid = ?',  (str(self.id), ))
            for row in c.fetchall():
                self.credits.append(Credit(row[0], row[1], row[2],  row[3],  row[4], row[5], row[6], row[7], self.eo))
    def updateJobList(self):
        self.jobs = []
        if self.eo is None:
            c.execute('select * from job WHERE companyid = ? ORDER BY startdate',  (str(self.id), ))
            for row in c.fetchall():
                self.jobs.append(Job(row[0], row[1], row[2], row[3], row[4],  row[5],  row[6],  row[7],  row[8],row[9], row[10],  row[11] , row[12], row[13], self.eo))
        else:
            sString = "select * from job WHERE jid = ?;"
            c.execute('select jid, companyid from job;')
            for r in c.fetchall():
                if self.eo.decrypt(r[1]) == str(self.id):
                    c.execute(sString,  (str(r[0]), ))
                    for row in c.fetchall():
                        self.jobs.append(Job(row[0], self.eo.decrypt(row[1]), self.eo.decrypt(row[2]), self.eo.decrypt(row[3]), self.eo.decrypt(row[4]),self.eo.decrypt(row[5]),  self.eo.decrypt(row[6]),self.eo.decrypt(row[7]), self.eo.decrypt(row[8]),self.eo.decrypt(row[9]),self.eo.decrypt(row[10]), self.eo.decrypt(row[11]),self.eo.decrypt(row[12]), row[13], self.eo))
    def updatechargesList(self):
        self.charges = []
        if self.eo!= None:
            sString = "select * from charges WHERE sid = ?;"
            c.execute('select sid, companyid from charges;')
            for r in c.fetchall():
                if self.eo.decrypt(r[1]) == str(self.id):
                    c.execute(sString,  (str(r[0]), ))
                    for row in c.fetchall():
                        self.charges.append(charges(row[0], self.eo.decrypt(row[1]), self.eo.decrypt(row[2]), encrypted=row[3], eo=self.eo))
        else:
            #self, id,  name,  value, wchargeid, howManyTimes, encrypted, eo)
            c.execute('select * from charges WHERE companyid = ?',  (str(self.id), ))
            for row in c.fetchall():
                self.charges.append(charges(row[0], row[1], row[2], -1,-1,encrypted,  self.eo))
    def createJob(self,  name, place, comment,  hours, correctionHours,  weekendDays,  startdate,  enddate,  leader,  active):
        # (self,  id,  name,  place,  comment,  hours, correctionHours,   startdate,  enddate,  baustellenleiter,  active, companyid):
        try:
            if self.eo != None:
                c.execute("INSERT INTO job (name, place, comment,hours, correctionHours, weekendDays, startdate, enddate,  leader, active, companyid, encrypted) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",  (self.eo.encrypt(name), self.eo.encrypt(place),  self.eo.encrypt(comment), self.eo.encrypt(hours),self.eo.encrypt(correctionHours),  self.eo.encrypt(weekendDays),  self.eo.encrypt(startdate), self.eo.encrypt(enddate),  self.eo.encrypt(leader), self.eo.encrypt(active),self.eo.encrypt(self.id),encrypted))
            else:
                c.execute("INSERT INTO job (name, place, comment,hours, correctionHours, weekendDays, startdate, enddate,  leader, active, companyid,encrypted) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",  (name, place,  comment, hours,correctionHours,  weekendDays,  startdate, enddate,  leader, active,   self.id,encrypted))
            db.commit()
            self.updateJobList()
        except sqlite3.Error as e:
            if e.args[0] == "column name is not unique":
                return -2
            else:
                print("An DB-error occurred:", e.args[0])
                return -1
        #except Exception as e:
            #print("An Error occurred:", e.args[0])
    def createSpese(self,  name, value, companyid = -10):
        try:
            if companyid != -10:
                if self.eo != None:
                    c.execute("INSERT INTO charges (name, value, companyid, encrypted) VALUES (?,?,?,?)",  ( self.eo.encrypt(name), self.eo.encrypt(value),  self.eo.encrypt(companyid), encrypted))
                else:
                    c.execute("INSERT INTO charges (name, value, companyid, encrypted) VALUES (?,?,?,?)",  ( name, value,  companyid, encrypted))
            else:
                if self.eo != None:
                    c.execute("INSERT INTO charges (name, value, companyid, encrypted) VALUES (?,?,?,?)",  ( self.eo.encrypt(name), self.eo.encrypt(value),  self.eo.encrypt(self.id), encrypted))
                else:
                    c.execute("INSERT INTO charges (name, value, companyid, encrypted) VALUES (?,?,?,?)",  ( name, value,  self.id, encrypted))
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
            if self.eo != None:
                c.execute("INSERT INTO loanSplit (name, value, money, companyid, encrypted) VALUES (?,?,?,?,?)",  ( self.eo.encrypt(name), self.eo.encrypt(value), self.eo.encrypt(tmpMoney),  self.eo.encrypt(self.id), encrypted))
            else:
                c.execute("INSERT INTO loanSplit (name, value, money, companyid, encrypted) VALUES (?,?,?,?,?)",  ( name, value, tmpMoney,  self.id, encrypted))
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
                if self.eo != None:
                    c.execute("INSERT INTO credit (name, value, date, payed,active, companyid,encrypted) VALUES (?,?,?,?,?,?,?)",  ( self.eo.encrypt(name),  self.eo.encrypt(value), self.eo.encrypt(date), self.eo.encrypt(tmpPayed),self.eo.encrypt(tmpActive),  self.eo.encrypt(companyid), encrypted))
                else:
                    c.execute("INSERT INTO credit (name, value, date, payed,active, companyid, encrypted) VALUES (?,?,?,?,?,?,?)",  ( name,  value, date, tmpPayed,tmpActive,  companyid, encrypted))
            else:
                if self.eo != None:
                    c.execute("INSERT INTO credit (name, value, date, payed,active, companyid,encrypted) VALUES (?,?,?,?,?,?,?)",  ( self.eo.encrypt(name),  self.eo.encrypt(value), self.eo.encrypt(date), self.eo.encrypt(tmpPayed),self.eo.encrypt(tmpActive),  self.eo.encrypt(self.id), encrypted))
                else:
                    c.execute("INSERT INTO credit (name, value, date, payed,active, companyid, encrypted) VALUES (?,?,?,?,?,?,?)",  ( name,  value, date, tmpPayed,tmpActive,  self.id, encrypted))
            db.commit()
        except sqlite3.Error as e:
            print("create credit An DB-error occurred:", e.args[0])
            return -1
    
    def save(self, name,  loan,  perHours, describtion):
        if self.eo!= None:
            c.execute("UPDATE company SET name=?, loan=?, perHours=?, describtion=?, encrypted=? WHERE cid=?",  (self.eo.encrypt(name), self.eo.encrypt(loan), self.eo.encrypt(perHours), self.eo.encrypt(describtion),encrypted,   self.id))
        else:
            c.execute("UPDATE company SET name=?, loan=?, perHours=?, describtion=?, encrypted=? WHERE cid=?",  (name, loan, perHours, describtion, encrypted,  self.id))
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
    def __init__(self,  id,  name,  place,  comment,  hours, correctionHours, weekendDays,  startdate,  enddate,  leader,  active, archived,  companyid, encrypted, eo):
        self.id = id
        self.name = name
        self.eo = eo
        self.place = place
        self.comment = comment
        self.hours = float(hours)
        self.correctionHours = float(correctionHours)
        self.weekendDays = int(weekendDays)
        self.startdate = QtCore.QDate.fromString(startdate, dbDateFormat)
        self.enddate = QtCore.QDate.fromString(enddate, dbDateFormat)
        self.leader = leader
        self.active = False
        if active == "1":
            self.active = True
        self.archived = False
        self.encrypted=encrypted
        if archived == "1":
            self.archived = True
        self.companyid = companyid
        self.updateWchargesList()
    def updateWchargesList(self):
        self.wcharges = []
        if self.eo != None:
            c.execute('select * from wcharges')
            for tmp1 in c.fetchall():
                if self.eo.decrypt(tmp1[1]) == str(self.id):
                    c.execute('select * from charges where sid=?', (self.eo.decrypt(tmp1[2]),  ))
                    for tmp2 in c.fetchall():
                        self.wcharges.append(charges(tmp2[0], self.eo.decrypt(tmp2[1]), self.eo.decrypt(tmp2[2]), tmp1[0], self.eo.decrypt(tmp1[3])))
        else:
            c.execute('select * from wcharges WHERE jobid = ?',  (str(self.id), ))
            for co in c.fetchall():
                c.execute('select * from charges WHERE sid = ?',  (str(co[2])))
                for row in c.fetchall():
                    self.wcharges.append(charges(row[0], row[1], row[2], co[0], co[3]))
    def addSpese(self,  chargesid, howManyTimes):
        if self.eo != None:
            c.execute("INSERT INTO wcharges (jobid, chargesid, howManyTimes,encrypted) VALUES (?,?,?,?)",  ( self.eo.encrypt(self.id), self.eo.encrypt(chargesid), self.eo.encrypt(howManyTimes), encrypted))
        else:
            c.execute("INSERT INTO wcharges (jobid, chargesid, howManyTimes,encrypted) VALUES (?,?,?,?)",  ( self.id, chargesid, howManyTimes, encrypted))
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
                    if self.eo != None:
                        c.execute("UPDATE wcharges SET howManyTimes=? WHERE wid=?",  (self.eo.encrypt(howManyTimes),  self.eo.encrypt(wcharge.wchargeId)))
                    else:
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
                if self.eo != None:
                    c.execute("UPDATE job SET name=?, place=?, comment=?, hours=?, correctionHours=?, weekendDays=?, startdate=?, enddate=?, leader=?, active=?, companyid=? WHERE jid=?",  (self.eo.encrypt(name), self.eo.encrypt(place),  self.eo.encrypt(comment), self.eo.encrypt(hours), self.eo.encrypt(correctionHours), self.eo.encrypt(weekendDays),  self.eo.encrypt(startdate), self.eo.encrypt(enddate), self.eo.encrypt(leader), self.eo.encrypt(tmpActive), self.eo.encrypt(companyid), self.id))
                else:
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
        
