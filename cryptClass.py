from header import *
import base64
import sys
#'cryptoclass - cm = cryptoMeta'
class cm:
    def __init__(self, pyCryptoModule,  key):
        self.key = key
        self.mod = pyCryptoModule
        if key != "":
            self.key = self.setKey(key)

        self.name = self.mod.__name__[14:]
        logger.debug("Init cm/cryptoMeta with module "+self.name)
        from Crypto import Random as rand
        self.rand = rand

    def setKey(self, key):
        self.key = key
        if len(self.key) < self.mod.block_size:
            rest = (self.mod.block_size *2) - len(self.key)
        else:
            rest = 16
        while rest !=0:
            rest -=1
            self.key += "."
        return self.key

    def encrypt(self, rawMessage):
        message=str(rawMessage)
        if self.mod == None:
            return rawMessage
        iv = self.rand.new().read(self.mod.block_size)
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
        if clearText[0:2] == "b'":
            clearText = clearText[2:-1]
        else:
            clearText = clearText[0:-1]
        #print("d "+self.name+clearText.rstrip())
        return clearText.rstrip()

#static crypt manager
class scm:
    #oldMod - self.encryptionObject,
    @staticmethod
    def updateAll(newCm, controller):
        controller.encryptionObject = newCm
        controller.updateEos(newCm)
        for company in controller.companylist:
            company.save(company.name,  company.loan, company.perHours, company.describtion)
            for charge in company.charges:
                charge.save( charge.name, charge.value,  charge.howManyTimes)
            for job in company.jobs:
                job.save( job.name, job.place, job.comment, job.hours, job.correctionHours, job.weekendDays,  job.startdate, job.enddate,job.leader, job.active, job.companyid)
                for wCharge in job.wcharges:
                    wCharge.save( wCharge.name,  wCharge.howManyTimes)
            for ls in company.loanSplits:
                ls.save( ls.name, ls.value,  ls.money)
            for credit in company.credits:
                credit.save(credit.name,  credit.value, credit.date, credit.payed, credit.active, company.id)
        for pf in controller.personalFinances:
            pf.save(pf.name, pf.value, pf.date, pf.repeat, pf.timesRepeat, pf.plusMinus, pf.active)

    @staticmethod
    def getMod(configValue):
        configValue = configValue.lower()
        try:
            if configValue == "1" or configValue == "aes":
                if("AES" not in sys.modules):
                    from Crypto.Cipher import AES
                return AES
            elif configValue == "2"  or configValue == "blowfish":
                if("Blowfish" not in sys.modules):
                    from Crypto.Cipher import Blowfish
                return Blowfish
            elif configValue == "3"  or configValue == "des3":
                if("DES3" not in sys.modules):
                    from Crypto.Cipher import DES3
                return DES3
            else:
                return None
        except  Exception as e:
            print(tr("Couldn't import pyCrypto, use plaintext Message; "))
            print(e)
