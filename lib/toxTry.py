from tox import Tox
from time import sleep
from lib.header import *
from os.path import exists
SERVER = ["54.199.139.199", 33445, "56A1ADE4B65B86BCD51CC73E2CD4E542179F47959FE3E0E21B4B0ACDADE5185520B3E6FC5D64"]
class ToxTry(Tox):
  def __init__(self,ui):
      self.ui=ui
      self.currentId = ""
      
      self.ui.toxTryChat.append("Alive!")
      if exists('toxData.sqlite'):
        self.load_from_file('toxData.sqlite')
      self.set_name("ToxTry")
      self.ui.toxTryId.setText(self.get_address())
      self.bootstrap_from_address(SERVER[0], 1, SERVER[1], SERVER[2])

  def loop(self):
    checked = False

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
        self.save_to_file('toxData.sqlite')
  def on_friend_request(self, pk, message):
      self.ui.toxTryChat.append('Friend request from %s: %s' % (pk, message))
      self.add_friend_norequest(pk)
      self.ui.toxTryChat.append('Accepted.')

  def on_friend_message(self, friendId, message):
      name = self.get_name(friendId)
      self.currentId = friendId
      self.ui.toxTryChat.append('%s: %s' % (name, message))