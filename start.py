#this code is GPL-FORCED so let changes open, pls!!
#License @ http://www.gnu.org/licenses/gpl.txt
#Author: skamster

import os.path,  sys
from models import *
from gui_class import *

app = QtGui.QApplication(sys.argv)
lang = ""
for config in mightyController.configlist:
    if config.key == "lang" or config.key == "language":
        if os.path.isfile(config.value):
            lang=config.value
        elif os.path.isfile(config.value+".qm"):
            lang=config.value+".qm"
translator = QtCore.QTranslator()
translator.load(lang,"./")
app.installTranslator(translator)
jobman = Gui()
jobman.show()

sys.exit(app.exec_())
