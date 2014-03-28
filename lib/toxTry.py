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
      self.toxUserlistUpdateTimes=4
      self.toxUserlistUpdateCounter=0
      self.currentToxUser = None
      self.ui.toxTryChat.append("Alive! toxTry-Thread started!")
      if exists('./toxData'):
        self.load_from_file('./toxData')
      else:
        self.set_name("ToxTry")
      self.ui.toxTryUsername.setText(self.get_self_name())
      self.ui.toxTryId.setText(self.get_address())
      self.updateToxUserObjects()
      self.updateToxUsers()
        #self.add_friend_norequest(tUser.pubKey)
      self.save_to_file('toxData')
      self.ui.toxTryFriends.itemClicked.connect(self.onClickToxUser)
      self.ui.toxTrySendButton.clicked.connect(self.onSendToxMessage)
      self.ui.toxTrySendText.returnPressed.connect(self.onSendToxMessage)
      self.ui.toxTryUsername.returnPressed.connect(self.onSaveToxUsername)
      self.ui.toxTryNewFriendRequest.clicked.connect(self.onNewFriendRequest)
      self.bootstrap_from_address(SERVER[0], 1, SERVER[1], SERVER[2])
  
  def getToxUserByFriendId(friendId):
    for tu in self.toxUserList:
      if tu.friendId == friendId:
        return tu
      
  def onNewFriendRequest(self):
    pk = QtGui.QInputDialog()
    #attention, tuples!!!
    pubKey = pk.getText(QtGui.QWidget(),"Add new friend","Please enter your friends tox-id")
    pubKey = pubKey[0]
    msg = QtGui.QInputDialog()
    message = msg.getText(QtGui.QWidget(),"Add a message","Send your friend a first message too.",text="I would like to add u to my list")
    message = message[0]
    #logger.error(str(pubKey)+ "    " +str(message))
    self.add_friend(str(pubKey),str(message))
    self.save_to_file('toxData')
    self.updateToxUserObjects()
    self.updateToxUsers()
    logger.error("add and update user")
  def updateToxUserObjects(self):
    self.toxUserList = []
    for friendId in self.get_friendlist():
      fid = friendId
      tu = toxUser(fid,self.get_name(fid),self.get_client_id(fid),self.get_user_status(fid),self.get_status_message(fid))
      self.toxUserList.append(tu)
  def updateToxUsers(self):
    self.ui.toxTryFriends.clear()
    for tu in self.toxUserList:
      self.ui.toxTryFriends.addItem("debugFake")
      self.ui.toxTryFriends.addItem("debugFake2")
      if tu.name == "":
        item1 = QtGui.QListWidgetItem(tu.pubKey)
        self.ui.toxTryFriends.addItem(item1)
        item1.setData(3, str(tu.statusMessage))
        if tu.status < 3:
          item1.setData(8, QtGui.QColor(51,255,0))
        else:
          item1.setData(8, QtGui.QColor(255,0,51))
      else:
        item1 = QtGui.QListWidgetItem(tu.name)
        self.ui.toxTryFriends.addItem(item1)
        item1.setData(3, str(tu.statusMessage))
        if tu.status < 3:
          item1.setData(8, QtGui.QColor(51,255,0))
        else:
          item1.setData(8, QtGui.QColor(255,0,51))
    sleep(.1)
        
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
        self.currentToxUser = tu
        self.ui.toxTryFriendInfos.clear()
        self.ui.toxTryFriendInfos.append("Name: "+tu.name)
        self.ui.toxTryFriendInfos.append("Public key: "+tu.pubKey)
        self.ui.toxTryFriendInfos.append("Status message: "+self.statusResolver(tu.status))
        self.ui.toxTryFriendInfos.append("Status message: "+tu.statusMessage)
        self.currentToxUser = tu
        if tu.status < 3:
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
                #self.connect()
                checked = False

            self.do()
            sleep(0.02)
    except Exception as e:
        logger.error(e.args[0])
        self.save_to_file('toxData')
        self.kill()
  def on_friend_request(self, pk, message):
      logger.error("friendrequest")
      self.ui.toxTryNotifications.append('Friend request from %s: %s' % (pk, message))
      self.add_friend_norequest(pk)
      #self.tmc.addToxUser("name",pk,message)
      self.save_to_file('toxData')
      self.ui.toxTryNotifications.append('Accepted friend request')

  #def on_connection_status(friendId, status):
    
  def on_friend_message(self, friendId, message):
      logger.error("friendmessage")
      name = self.get_name(friendId)
      self.currentId = friendId
      self.ui.toxTryChat.append('%s: %s' % (name, message))
      
  def on_name_change(self,friendId,name):
      self.ui.toxTryNotifications.append("Name changed to "+name)
      if self.currentToxUser is not None:       self.currentToxUser.name=name
      logger.error("namechange")
      self.updateToxUsers()
  def on_user_status(self, friendId,status):  
      if self.currentToxUser is not None:       self.currentToxUser.status=status
      logger.error("status")
      self.updateToxUsers()
      
  def on_status_message(self,friendId, statusMessage):  
      if self.currentToxUser is not None:       self.currentToxUser.statusMessage=statusMessage
      logger.error("statusmessage")
      self.updateToxUsers()  
  def on_group_invite(friendId,groupPk):
    logger.error("becoming group invite")
    self.join_groupchat(friendId,groupPk)
    
  