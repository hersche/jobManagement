import os.path,sqlite3
from lib.header import *
from PyQt4.QtCore import pyqtSlot,pyqtSignal
fileExist = True
if os.path.isfile('toxMessages.db') == False:
    #..und ggf umgestellt..
    fileExist = False
#..denn sqlite3.connect erstellt immer ein file!
db2 = sqlite3.connect('toxMessages.db')
#aber wir brauchen ja den cursor, um die db initialisieren zu können.
c2 = db2.cursor()
if fileExist == False:
    c2.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY, friendId int, timestamp text, message text, me integer, encrypted text)")

class toxMessageHandler(QtCore.QObject):
  toxMessageArrived = pyqtSignal(object)
  toxMessageDbUpdate = pyqtSignal(object)
  def __init__(self):
    QtCore.QObject.__init__(self)
    self.cachedToxMessages=[]
    self.tmpFriendId = -1
    self.toxMessageArrived.connect(self.flushMessage)
    self.toxMessageDbUpdate.connect(self.updateMessages)
  def updateToxUsers(self):
    logger.debug("disabled method.")
    
  def addMessage(self,toxMessage):
    self.cachedToxMessages.append(toxMessage)
    self.toxMessageArrived.emit(toxMessage)
    
  def kickUpdate(self,friendId):
      self.tmpFriendId = friendId
      self.toxMessageDbUpdate.emit(friendId)
  def updateMessages(self):
    self.messages = []
    c2.execute('select * from messages where friendId='+str(self.tmpFriendId)+';')
    for msg in c2.fetchall():
      self.messages.append(toxMessage(msg[1],msg[2],msg[3],msg[4]))
  def flushMessage(self):
    try:
      #logger.error("signal catched, write now!")
      for toxMessage in self.cachedToxMessages:
        if toxMessage.me:       tmpBoolMe = 1
        else:   tmpBoolMe = 0
        c2.execute("INSERT INTO messages (friendId, timestamp, message,me, encrypted) VALUES (?,?,?,?,?)",  ( toxMessage.friendId, toxMessage.timestamp,  toxMessage.message,tmpBoolMe, "-1"))
      db2.commit()
      self.cachedToxMessages=[]
    except sqlite3.Error as e:
      logger.error("An DB-error occurred: "+e.args[0])
    
class toxMessage:
  def __init__(self,friendId,message, timestamp,me):
      if me == 0:
        self.me = False
      else:
        self.me = True
      #logger.error("message created, timestamp "+timestamp)
      self.friendId=friendId
      self.message = message
      self.timestamp = timestamp


    
 