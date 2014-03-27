import os.path,sqlite3
from lib.header import *
fileExist = True
if os.path.isfile('toxModels.db') == False:
    #..und ggf umgestellt..
    fileExist = False
#..denn sqlite3.connect erstellt immer ein file!
db2 = sqlite3.connect('toxModels.db')
#aber wir brauchen ja den cursor, um die db initialisieren zu können.
c2 = db2.cursor()
if fileExist == False:
    c2.execute("CREATE TABLE toxUser (tuid  INTEGER PRIMARY KEY, name text UNIQUE, pubKey text, status text, encrypted text)")
    c2.execute("CREATE TABLE toxMessage (mtid INTEGER PRIMARY KEY, message text, date text,tuid text, encrypted text)")

class toxController:
  def __init__(self,name,pubKey):
    self.name = name
    self.pubKey = pubKey
    self.updateToxUsers()
  def updateToxUsers(self):
    self.toxUserList = []
    c2.execute('select * from toxUser')
    for tUser in c2.fetchall():
      self.toxUserList.append(toxUser(tUser[0],tUser[1],tUser[2],tUser[3]))
  def createToxUser(self,name, pubKey,status):
    try:
      logger.error("appears in createToxUser")
      c2.execute("INSERT INTO toxUser (name, pubKey, status, encrypted) VALUES (?,?,?,?)",  ( name, pubKey,  status, "-1"))
      db2.commit()
    except sqlite3.Error as e:
      logger.error("An DB-error occurred: "+e.args[0])
    

class toxUser:
  def __init__(self,id,name, pubKey,status):
    self.id = id
    self.name = name
    self.pubKey = pubKey
    self.status = status
  def save(self,name, pubKey,status):
    c2.execute("UPDATE toxUser SET name=?, pubKey=?,status=? WHERE tuid=?",  (name, pubKey,status, self.id))
    db2.commit()
    
 