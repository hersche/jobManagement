import sqlite3
db = sqlite3.connect('jobmanagement.db')
c = db.cursor()
class Controller:
        def __init__(self):
            self.updateList()
        def createCompany(self, name,  loan,  perHours,  describtion):
            c.execute("INSERT INTO company (name, loan,  perHours, describtion) VALUES (?,?,?,?);",  (name, loan,  perHours, describtion))
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
                    
class config:
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
        if payed == True:
            tmpPayed = 1
        else:
            tmpPayed = 0
            c.execute("INSERT INTO credit (value, date, payed, companyid) VALUES (?,?,?,?)",  ( value, date, tmpPayed, self.id))
            db.commit()
    
    def save(self, name,  loan,  perHours, describtion):
            c.execute("UPDATE company SET name=?, loan=?, perHours=?, describtion=? WHERE cid=?",  (name, loan, perHours, describtion,  self.id))
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
