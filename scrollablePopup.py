
from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class scrollablePopup(QScrollArea):

	def __init__(self) -> None:
		super(__class__, self).__init__()
		self._widget = QWidget()
		self._layout = QVBoxLayout(self._widget)
		self._layout.setAlignment(Qt.AlignTop)
		self._label = QLabel()
		self._layout.addWidget(self._label)
		self.setWidget(self._widget)
		self.setWidgetResizable(True)
		self.setFixedWidth(530)
		self.setFixedHeight(630)
		
	def setText(self, text: str) -> None:
		self._label.setText(text)
		
	def setTitle(self, title: str) -> None:
		self.setWindowTitle(title)