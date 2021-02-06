"""

https://www.dr-lex.be/info-stuff/videocalc.html
http://www.3ivx.com/support/calculator/index.html
https://www.silverjuke.net/public/misc/bitrate-calculator.html
https://www.colincrawley.com/audio-file-size-calculator/

Bitrate Calculator
by Gabriel Christo

				(bitrate in desired unit)
Pixel size =	---------------------------------------------------------------------
				(length in seconds) * (frames per second) * (resolution total pixels)

				(bitrate in desired unit)
Sample size =	--------------------------------------------
				(length in seconds) * (sample rate in hertz)

Audio size =	(bitrate in desired unit) * (length in seconds)

Video bitrate =		(desired video size)
					--------------------
					(length in seconds)


Bits per pixel explained:
< 0.10: High probability result in poor quality
0.10 - 0.15: It will look average to bad
0.15 - 0.20: You will notice blocks, but it will look okay
0.20 - 0.25: It will look really good
0.25 - 0.30: It won't really improve visually
> 0.30: Don't do that either - try a bigger resolution instead

"""

from typing import Tuple, List, Dict

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QObject, Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from constants import *

# todo: expandir resolucoes
PixelsByResolution = {"hd1080": 2073600,
"hd720": 921600,
"hd480": 409920,
"vga": 307200,
"qvga": 76800}

class ByteConverter():

	def __init__(self): self._bytes = 0
	def to_bit(self) -> float: return self._bytes * 8
	def to_kilo_bit(self) -> float: return self._bytes / 125
	def to_kilo_byte(self) -> float: return self._bytes / 1000
	def to_mega_byte(self) -> float: return self._bytes / 1e6
	def to_giga_byte(self) -> float: return self._bytes / 1e9
	def set_kilo_bit(self, value: float) -> None: self._bytes = value * 125
	def set_mega_bit(self, value: float) -> None: self._bytes = value * 125000
	def set_mega_byte(self, value: float) -> None: self._bytes = value * 1e6
	def set_giga_byte(self, value: float) -> None: self._bytes = value * 1e9


class BitrateCalculator(QMainWindow):

	def __init__(self):
		super(__class__, self).__init__()
		uic.loadUi("./bitrateCalculator.ui", self)
		self.setWindowTitle("Bitrate Calculator")
		self.setWindowIcon(QIcon(ICON))
		self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
		self.byteConverter = ByteConverter()
		self.connects()
		
		# hiding not being used widgets at UI
		self.vBitrateInputLabel.setVisible(False)
		self.vBitrateLine.setVisible(False)
		self.vBitrateCombo.setVisible(False)
		self.aChannelsLabel.setVisible(False)
		self.aSampleRateLabel.setVisible(False)
		self.aRateCombo.setVisible(False)
		self.hzLabel.setVisible(False)
		self.aChannelsSpinbox.setVisible(False)
	
	def connects(self) -> None:
		# any modification on input fields will recalculate the file size
		self.hourLine.textChanged.connect(self.calculate_file_size)
		self.minuteLine.textChanged.connect(self.calculate_file_size)
		self.secondLine.textChanged.connect(self.calculate_file_size)
		self.fpsSpinbox.valueChanged.connect(self.calculate_file_size)
		self.resolutionCombo.currentTextChanged.connect(self.calculate_file_size)
		self.desiredVSize.textChanged.connect(self.calculate_file_size)
		self.aBitrateCombo.currentTextChanged.connect(self.calculate_file_size)
		self.desiredVSizeCombo.currentTextChanged.connect(self.calculate_file_size)
	
	def update_seconds_label(self) -> int:
		crrtHours = self.str_to_int(self.hourLine.text())
		crrtMinutes = self.str_to_int(self.minuteLine.text())
		crrtSeconds = self.str_to_int(self.secondLine.text())
		total = self.hms_to_seconds(crrtHours, crrtMinutes, crrtSeconds)
		self.totalSecondsLabel.setText(str(total))
		return total
		
	@pyqtSlot()
	def calculate_file_size(self) -> None:
	
		seconds = self.update_seconds_label()
		if seconds == 0: seconds = 1 # avoid division by zero
		finalSizeInMB = 0
		
		##### video size #####
		
		# desired video size
		vSize = self.str_to_float(self.desiredVSize.text())
		if self.desiredVSizeCombo.currentText() == "MB": self.byteConverter.set_mega_byte(vSize)
		elif self.desiredVSizeCombo.currentText() == "GB": self.byteConverter.set_giga_byte(vSize)
		finalSizeInMB += self.byteConverter.to_mega_byte()
		
		# setting recommended video bitrate
		vBitrate = self.truncate(self.byteConverter.to_kilo_bit() / seconds, 2)
		self.byteConverter.set_kilo_bit(vBitrate)
		self.videoBitrateLabel.setText("~ " + str(vBitrate) + " kbps")
		
		# calculating bit per pixel (based on resolution and fps)
		fps = self.fpsSpinbox.value()
		pixels = PixelsByResolution[self.resolutionCombo.currentText()]
		
		pixels_per_second = (fps * pixels)
		pixel_size = self.truncate(self.byteConverter.to_bit() / pixels_per_second, 3)
		self.bitPerPixel.setText(str(pixel_size) + " bits per pixel")
		
		##### audio size #####
		
		# sample rate, bit depth and channels only used to lossless codecs
		# todo: add lossless and lossy size
		# todo:add bit depth
		sample_rate = self.str_to_int(self.aRateCombo.currentText())
		channels = self.aChannelsSpinbox.value()
		
		# calculating audio size in MB
		audio_bitrate = self.str_to_int(self.aBitrateCombo.currentText())
		audio_size = audio_bitrate * seconds # audio in kbps
		self.byteConverter.set_kilo_bit(audio_size)
		audio_in_MB = self.byteConverter.to_mega_byte()
		finalSizeInMB += audio_in_MB
		audio_size_str = "~ " + str(audio_in_MB) + " MB"
		self.audioSizeLabel.setText(audio_size_str)
		
		##### final size #####
		if(finalSizeInMB >= 1024):
			self.byteConverter.set_mega_byte(finalSizeInMB)
			self.finalSizeLabel.setText("~ " + str(self.truncate(self.byteConverter.to_giga_byte(), 2)) + " GB")
		else: self.finalSizeLabel.setText("~ " + str(self.truncate(finalSizeInMB, 2)) + " MB")
		
		
	def hms_to_seconds(self, hours: int, minutes: int, seconds: int) -> int:
		return hours*3600 + minutes*60 + seconds
		
	
	def str_to_int(self, string: str) -> int:
		try:
			value = int(string)
			return value
		except ValueError:
			if DEBUG: print("ValueError on str_to_int")
			return 0
		
	def str_to_float(self, string: float) -> float:
		try:
			value = float(string)
			return value
		except ValueError:
			if DEBUG: print("ValueError on str_to_float")
			return 0
			
	def truncate(self, n, decimals=0):
		multiplier = 10 ** decimals
		return int(n * multiplier) / multiplier
			
			
			
	