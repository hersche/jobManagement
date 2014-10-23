#this code is GPL-FORCED so let changes open, pls!!
#License @ http://www.gnu.org/licenses/gpl.txt
#Author: skamster

from lib.guiController import *
from lib.models import Config
import sys

singleView = False
singleViewId = -1
lang = Config.getConfigByKey("lang")
if lang==None:
  lang = Config.getConfigByKey("language")
app = QtWidgets.QApplication(sys.argv)
translator = QtCore.QTranslator()
if lang is not None:
  translator.load(lang.value,"./lang/")
  app.installTranslator(translator)
gui = Gui()
gui.show()

sys.exit(app.exec_())
