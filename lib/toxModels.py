import os.path,sqlite3
from lib.header import *
from PyQt4.QtCore import pyqtSlot,pyqtSignal
fileExist = True
if os.path.isfile('toxModels.db') == False:
    #..und ggf umgestellt..
    fileExist = False
#..denn sqlite3.connect erstellt immer ein file!
db2 = sqlite3.connect('toxModels.db')
#aber wir brauchen ja den cursor, um die db initialisieren zu können.
c2 = db2.cursor()
if fileExist == False:
    c2.execute("CREATE TABLE toxUser (tuid  INTEGER PRIMARY KEY, name text, pubKey varchar(190) UNIQUE, status text, encrypted text)")
    c2.execute("CREATE TABLE toxMessage (mtid INTEGER PRIMARY KEY, message text, date text,tuid text, encrypted text)")

class toxController(QtCore.QObject):
  toxuserappend = pyqtSignal(object)
  def __init__(self,name,pubKey):
    QtCore.QObject.__init__(self)
    self.name = name
    self.pubKey = pubKey
    self.updateToxUsers()
    self.cachedToxUsers=[]
    self.toxuserappend.connect(self.flushToxUser)
  def updateToxUsers(self):
    logger.debug("disabled method.")
    #self.toxUserList = []
    #c2.execute('select * from toxUser')
    #for tUser in c2.fetchall():
      #self.toxUserList.append(toxUser(tUser[0],tUser[1],tUser[2],tUser[3]))
  def addToxUser(self,name, pubKey,status):
    logger.debug("|CryptModel| Add user to cache and give signal to save. Origpubkey is "+str(len(pubKey)))
    self.cachedToxUsers.append(toxUser(-1,name, pubKey,status))
    self.toxuserappend.emit(toxUser(-1,name, pubKey,status))
  def flushToxUser(self):
    try:
      for tU in self.cachedToxUsers:
        c2.execute("INSERT INTO toxUser (name, pubKey, status, encrypted) VALUES (?,?,?,?)",  ( tU.name, tU.pubKey,  tU.status, "-1"))
        logger.error("unsafed, but right before "+str(len(tU.pubKey)))
      db2.commit()
      self.cachedToxUsers=[]
      self.updateToxUsers()
      for tU in self.toxUserList:
        logger.error("safed, but right after "+str(len(tU.pubKey)))
    except sqlite3.Error as e:
      logger.error("An DB-error occurred: "+e.args[0])
    

class toxUser:
  def __init__(self,friendId,name,pubKey,status,statusMessage):
    self.friendId = friendId
    self.name = name
    self.pubKey = pubKey
    self.status = status
    self.statusMessage = statusMessage
  def save(self,name, pubKey,status):
    c2.execute("UPDATE toxUser SET name=?, pubKey=?,status=? WHERE tuid=?",  (name, pubKey,status, self.id))
    db2.commit()
    
 