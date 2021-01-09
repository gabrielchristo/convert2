
import sys
from convert2 import *
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
	app = QApplication(sys.argv)
	with open("style.css", "r") as style: app.setStyleSheet(style.read())
	c2 = Convert2()
	c2.show()
	sys.exit(app.exec_())