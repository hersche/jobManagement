#this code is GPL-FORCED so let changes open, pls!!
#License @ http://www.gnu.org/licenses/gpl.txt
#Author: skamster

from gui_class import *
import sys
app = QtGui.QApplication(sys.argv)
translator = QtCore.QTranslator()
translator.load(lang,"./")
app.installTranslator(translator)
jobman = Gui()
jobman.show()

sys.exit(app.exec_())
