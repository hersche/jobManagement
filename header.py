from PyQt4 import QtCore,  QtGui
import re
from models import *
lang = ""
singleView = False
singleViewId = -1
singleViewName = ""
encrypted = -1
mightyController = Controller();
for config in mightyController.configlist:
    if (config.key.lower() == "single" or config.key.lower() == "singleview") and (config.value.lower() == "true" or config.value.lower() == "1"):
        singleView = True
        from gui_single import Ui_MainWindowSingle
    elif config.key.lower()== "singleviewcname":
        singleViewName = config.value
    elif config.key.lower()== "encrypted":
        try:
            from Crypto.Cipher import * 
            encrypted = config.value
        except:
            print(tr("Couldn't import pyCrypto, use plaintext"))
            encrypted = -1
    elif config.key.lower()== "singleviewcid":
        singleViewId = config.value
    elif config.key == "lang" or config.key == "language":
        if os.path.isfile(config.value):
            lang=config.value
        elif os.path.isfile(config.value+".qm"):
            lang=config.value+".qm"
if True is not singleView:
    from gui import Ui_MainWindow
