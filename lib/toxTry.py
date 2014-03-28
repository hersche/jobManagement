from tox import Tox
from time import sleep
from lib.header import *
from os.path import exists
SERVER = ["54.199.139.199", 33445, "56A1ADE4B65B86BCD51CC73E2CD4E542179F47959FE3E0E21B4B0ACDADE5185520B3E6FC5D64"]

class toxUser:
  def __init__(self,friendId,name,pubKey,status,statusMessage):
    self.friendId = friendId
    self.name = name
    self.pubKey = pubKey
    self.status = status
    self.statusMessage = statusMessage


class ToxTry(Tox):
  def __init__(self,ui):
      self.ui=ui
      self.currentToxUser = None
      self.ui.toxTryChat.append("Alive! toxTry-Thread started!")
      if exists('./toxData'):
        self.load_from_file('./toxData')
      else:
        self.set_name("ToxTry")
      self.ui.toxTryUsername.setText(self.get_self_name())
      self.ui.toxTryId.setText(self.get_address())
      self.updateToxUsers()
      self.updateToxUserObjects() 
        #self.add_friend_norequest(tUser.pubKey)
      self.save_to_file('toxData')
      self.ui.toxTryFriends.itemClicked.connect(self.onClickToxUser)
      self.ui.toxTrySendButton.clicked.connect(self.onSendToxMessage)
      self.ui.toxTrySendText.returnPressed.connect(self.onSendToxMessage)
      self.ui.toxTryUsername.returnPressed.connect(self.onSaveToxUsername)
      self.bootstrap_from_address(SERVER[0], 1, SERVER[1], SERVER[2])
      
  def updateToxUserObjects(self):
    self.toxUserList = []
    for friendId in self.get_friendlist():
      fid = friendId
      tu = toxUser(fid,self.get_name(fid),self.get_client_id(fid),self.get_user_status(fid),self.get_status_message(fid))
      self.toxUserList.append(tu)
  def updateToxUsers(self):
    self.ui.toxTryFriends.clear()
    for friendId in self.get_friendlist():
      fid = friendId
      self.ui.toxTryFriends.addItem("debugFake")
      self.ui.toxTryFriends.addItem("debugFake2")
      if self.get_name(fid) == "":
        item1 = QtGui.QListWidgetItem(self.get_client_id(fid))
        self.ui.toxTryFriends.addItem(item1)
        item1.setData(3, str(self.get_status_message(fid)))
        if self.get_user_status(fid) < 4:
          item1.setData(8, QtGui.QColor(51,255,0))
        else:
          item1.setData(8, QtGui.QColor(255,0,51))
      else:
        item1 = QtGui.QListWidgetItem(self.get_name(fid))
        self.ui.toxTryFriends.addItem(item1)
        item1.setData(3, str(self.get_status_message(fid)))
        if self.get_user_status(fid) < 4:
          item1.setData(8, QtGui.QColor(51,255,0))
        else:
          item1.setData(8, QtGui.QColor(255,0,51))
        
  def statusResolver(self,inti):
    if inti == 0:
      return "Online"
    elif inti == 1:
      return "Busy"
    elif inti == 2:
      return "Away"
    else:
      return "Invalid"
    
    
  def onSaveToxUsername(self):
    self.set_name(self.ui.toxTryUsername.text())
    self.save_to_file('toxData')
  def onSendToxMessage(self):
    message = self.ui.toxTrySendText.text()
    try:
      if self.currentToxUser is not None:
        self.send_message(self.currentToxUser.friendId, message)
        if self.currentToxUser.name != "":
          self.ui.toxTryChat.append(self.currentToxUser.name+": "+message)
        else:
          self.ui.toxTryChat.append(self.currentToxUser.pubKey+": "+message)
        self.ui.toxTrySendText.clear()
    except Exception as e:
      logger.error("Send Message failed: "+e.args[0])
  def onClickToxUser(self,item):
    txt = item.text()
    self.updateToxUserObjects()
    for tu in self.toxUserList:
      if tu.name == txt or tu.pubKey == txt:
        self.ui.toxTryFriendInfos.clear()
        self.ui.toxTryFriendInfos.append("Name: "+tu.name)
        self.ui.toxTryFriendInfos.append("Public key: "+tu.pubKey)
        self.ui.toxTryFriendInfos.append("Status message: "+self.statusResolver(tu.status))
        self.ui.toxTryFriendInfos.append("Status message: "+tu.statusMessage)
        self.currentToxUser = tu
        if tu.status < 4:
          item.setData(8, QtGui.QColor(51,255,0))
        else:
          item.setData(8, QtGui.QColor(255,0,51))
  def loop(self):
    checked = False
    try:
        while True:
            status = self.isconnected()
            if not checked and status:
                self.ui.toxTryNotifications.append('Connected to DHT.')
                checked = True
            if checked and not status:
                self.ui.toxTryNotifications.append('Disconnected from DHT.')
                self.connect()
                checked = False

            self.do()
            sleep(0.02)
    except KeyboardInterrupt:
        self.save_to_file('toxData')
  def on_friend_request(self, pk, message):
      self.ui.toxTryNotifications.append('Friend request from %s: %s' % (pk, message))
      self.add_friend_norequest(pk)
      #self.tmc.addToxUser("name",pk,message)
      self.save_to_file('toxData')
      self.ui.toxTryNotifications.append('Accepted friend request')

  #def on_connection_status(friendId, status):
    
  def on_friend_message(self, friendId, message):
      name = self.get_name(friendId)
      self.currentId = friendId
      self.ui.toxTryChat.append('%s: %s' % (name, message))
      
  def on_name_change(self,friendId,name):
    logger.error("|toxTry| name changed to "+name)
    self.updateToxUsers()
  def on_user_status(self, friendId,status):
    self.ui.toxTryNotifications.append("userStatus: "+str(status))
    self.updateToxUsers()
      
  def on_status_message(self,friendId, news):
      self.ui.toxTryNotifications.append("newsStatus: "+str(news))
      self.updateToxUsers()