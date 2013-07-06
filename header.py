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
