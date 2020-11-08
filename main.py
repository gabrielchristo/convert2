
import sys
from convert2 import *
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
	app = QApplication(sys.argv)
	c2 = Convert2()
	c2.show()
	sys.exit(app.exec_())