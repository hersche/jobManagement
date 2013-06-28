from PyQt4 import QtCore,  QtGui
from binascii import b2a_hex
import re
from models import *
def tr(name):
    return QtCore.QCoreApplication.translate("@default",  name)
lang = ""
singleView = False
singleViewId = -1
singleViewName = ""
encrypted = "-1"
iv = 0
pw = ""
mightyController = Controller();
for config in mightyController.configlist:
    if (config.key.lower() == "single" or config.key.lower() == "singleview") and (config.value.lower() == "true" or config.value.lower() == "1"):
        singleView = True
        from gui_single import Ui_MainWindowSingle
    elif config.key.lower()== "singleviewcname":
        singleViewName = config.value
    elif config.key.lower()== "encrypted":
        try:
            from Crypto import Random as rand
            if config.value == "1" or config.value == "AES":
                from Crypto.Cipher import AES as enc
                encrypted = "AES"
            elif config.value == "2"  or config.value == "Blowfish":
                from Crypto.Cipher import Blowfish as enc
                encrypted = "ARC4"
            elif config.value == "3"  or config.value == "DES3":
                from Crypto.Cipher import DES3 as enc
                encrypted = DES3
            else:
                encrypted = "-1"
            if encrypted != "-1":
                iv = rand.new().read(enc.block_size)
                print("iv-length: "+str(len(iv)))
        except  Exception as e:
            print(tr("Couldn't import pyCrypto, use plaintext Message; "))
            print(e)
            #encrypted = -1
    elif config.key.lower()== "singleviewcid":
        singleViewId = config.value
    elif config.key == "lang" or config.key == "language":
        if os.path.isfile(config.value):
            lang=config.value
        elif os.path.isfile(config.value+".qm"):
            lang=config.value+".qm"
if True is not singleView:
    from gui import Ui_MainWindow
