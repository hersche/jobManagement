from tox import Tox
from time import sleep
from lib.header import *
from os.path import exists
SERVER = ["54.199.139.199", 33445, "56A1ADE4B65B86BCD51CC73E2CD4E542179F47959FE3E0E21B4B0ACDADE5185520B3E6FC5D64"]

class ToxTry(Tox):
  def __init__(self,ui,tmc):
      self.ui=ui
      self.currentId = ""
      self.ui.toxTryChat.append("Alive! toxTry-Thread started!")
      if exists('./toxData'):
        self.load_from_file('./toxData')
      else:
        self.set_name("ToxTry")
      self.statusMsg = QtCore.SIGNAL("blaaa")
      self.ui.toxTryUsername.setText(self.get_self_name())
      self.ui.toxTryId.setText(self.get_address())
      #self.addPublicKey = QtCore.SIGNAL("addPublicKey")
      self.addPK = QtCore.pyqtSignal(str)
      for tUser in tmc.toxUserList:
        self.add_friend_norequest(tUser.pubKey)
      self.save_to_file('toxData')
      self.FriendRequest = [False,""]
      self.statusMessage=[False,"",""]
      self.bootstrap_from_address(SERVER[0], 1, SERVER[1], SERVER[2])

  def loop(self,tmc):
    checked = False
    self.tmc = tmc

    try:
        while True:

            status = self.isconnected()
            if not checked and status:
                self.ui.toxTryChat.append('Connected to DHT.')
                self.ui.toxTryChat.append('Waiting for friend request')
                checked = True

            if checked and not status:
                self.ui.toxTryChat.append('Disconnected from DHT.')
                self.connect()
                checked = False

            self.do()
            sleep(0.02)
    except KeyboardInterrupt:
        self.save_to_file('toxData')
  def on_friend_request(self, pk, message):
      self.ui.toxTryChat.append('Friend request from %s: %s' % (pk, message))
      self.add_friend_norequest(pk)
      #self.emit(self.addPublicKey, pk)
      #QtCore.QObject.addPK.emit(pk)
      self.FriendRequest = [True, pk]
      logger.error("here i create the user!")
      #self.tmc.createToxUser("as",pk,"aa")
      #self.emit(QtCore.SIGNAL("addPublicKey"), pk, pk)
      # self.toxModelController.createToxUser("",pk, "")
      self.save_to_file('toxData')
      self.ui.toxTryChat.append('Accepted.')

  def on_friend_message(self, friendId, message):
      name = self.get_name(friendId)
      self.currentId = friendId
      self.ui.toxTryChat.append('%s: %s' % (name, message))
      
  def on_user_status(self, friendId,kind):
      logger.error("userStatus: "+str(friendId)+" "+str(kind))
      
  def on_status_message(self,friendId, news):
      self.statusMessage=[True,friendId,news]
      emit(self.statusMsg)
      logger.error("newsStatus: "+str(friendId)+" "+str(news))
      #self.tmc.createToxUser(str(friendId),"publigg",str(news))