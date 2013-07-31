from header import *
from Crypto import Random as rand
import base64
from Crypto.Cipher import * 
#'cryptoclass - cm = cryptoMeta'
class cm:
    def __init__(self, key, pyCryptoModule):
        self.name = ""
        self.key = key
        self.mod = pyCryptoModule
        if len(self.key) < self.mod.block_size:
            rest = self.mod.block_size - len(self.key)
            print(str(rest))
            while rest !=0:
                rest -=1
                self.key += "."
        print(self.key)
    def setKey(self, key):
        self.key = key

    def pad(self,  s):
        bla = lambda s: s + (self.mod.block_size- len(s) % self.mod.block_size) * chr(self.mod.block_size - len(s) % self.mod.block_size)
        return bla
    def unpad(self, s):
        upad = lambda s : s[0:-ord(s[-1])]
        return upad
    def encrypt(self, rawMessage):
        message=str(rawMessage)
        if self.mod == None:
            return rawMessage
        iv = rand.new().read(self.mod.block_size)
        cipher = self.mod.new(self.key, self.mod.MODE_CBC, iv)
        mLen = len(message)
        if mLen > self.mod.block_size:
            rest = self.mod.block_size-(mLen% self.mod.block_size)
        else:
            rest = self.mod.block_size - mLen
        tmp = ""
        while rest != 0:
            rest -=1
            tmp += " "
        eMessage = message+tmp
        #print(eMessage+str(len(eMessage)))
        t =  base64.b64encode(iv + cipher.encrypt(eMessage))
        return t
    def decrypt(self, encryptedMessage):
        if self.mod == None:
            return encryptedMessage
        if encryptedMessage is None:
            return ""
        tDec = base64.b64decode(encryptedMessage)
        iv = tDec[:self.mod.block_size]
        cipher = self.mod.new(self.key, self.mod.MODE_CBC, iv)
        clearText = str(cipher.decrypt(tDec[self.mod.block_size:]))
        clearText = clearText[2:-1]
        return clearText.rstrip()
class scm:
    #oldMod - self.eo,
    @staticmethod
    def updateAll(newCm, controller):
        controller.eo = newCm
        for company in controller.companys:
            company.save(company.name,  company.loan, company.perHours, company.describtion)
            for charge in company.charges:
                charge.save( charge.name, charge.value,  charge.howManyTimes)
            for job in company.jobs:
                job.save( newCm.encrypt(job.name), job.place, job.comment, job.hours, job.correctionHours, job.weekendDays,  job.startdate, job.enddate,job.leader, job.active, job.companyid)
                for wCharge in job.wcharges:
                    wCharge.save( wCharge.name,  wCharge.howManyTimes)
                    
            for ls in company.loanSplits:
                ls.save( ls.name, ls.value,  ls.money)
            for credit in company.credits:
                credit.save(credit.name,  credit.value, credit.date, credit.payed, credit.active, company.id)
        for pf in controller.personalFinances:
            pf.save(pf.name, pf.value, pf.date, pf.repeat, pf.timesRepeat, pf.plusMinus, pf.active)
            print("static updatemethod")

    @staticmethod
    def getMod(configValue):
        configValue = configValue.lower()
        
        encrypted = "-1"
        try:
            if configValue == "1" or configValue == "aes":
                print("return mod" +configValue)
                from Crypto.Cipher import AES as enc
                encrypted = "AES"
            elif configValue == "2"  or configValue == "blowfish":
                from Crypto.Cipher import Blowfish as enc
                encrypted = "ARC4"
            elif configValue == "3"  or configValue == "des3":
                from Crypto.Cipher import DES3 as enc
                encrypted = "DES3"
            else:
                enc = None
                encrypted = "-1"
        except  Exception as e:
            print(tr("Couldn't import pyCrypto, use plaintext Message; "))
            print(e)
        print(enc)
        return enc
