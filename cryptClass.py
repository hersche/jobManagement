from header import *
import base64
#'cryptoclass - cm = cryptoMeta'
class cm:
    def __init__(self,   key, pyCryptoModule):
        self.name = ""
        self.key = key
        if len(key) < pyCryptoModule.block_size:
            rest = pyCryptoModule.block_size - len(key)
            print(str(rest))
            while rest !=0:
                rest -=1
        
                self.key += "."
        print(self.key+ str(len(self.key)))
        self.mod = pyCryptoModule
    def pad(self,  s):
        bla = lambda s: s + (self.mod.block_size- len(s) % self.mod.block_size) * chr(self.mod.block_size - len(s) % self.mod.block_size)
        return bla
    def unpad(self, s):
        upad = lambda s : s[0:-ord(s[-1])]
        return upad
    def encrypt(self, rawMessage):
        print("encrypt")
        message=str(rawMessage)
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
        print("decrypt "+str(encryptedMessage))
        if encryptedMessage is None:
            return ""
        tDec = base64.b64decode(encryptedMessage)
        iv = tDec[:self.mod.block_size]
        cipher = self.mod.new(self.key, enc.MODE_CBC, iv)
        clearText = str(cipher.decrypt(tDec[self.mod.block_size:]))
        clearText = clearText[2:-1]
        return clearText.rstrip()
class scm:
    @staticmethod
    def updateAll(oldMod, newMod, controller):
        for companys in controller.companys:
            print("static updatemethod")
