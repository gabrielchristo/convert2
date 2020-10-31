"""

Convert2 Tool
by Gabriel Christo
10/2020

TODO:
	video resolution combobox
	trim video -ss -to
	-[a,v,s]n to remove streams
	subtitle size/color

"""

import sys
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QInputDialog
from PyQt5.QtCore import pyqtSlot, Qt, QDir, QProcess

class CmdBuilder():
	
	def __init__(self):
		self.vcodec = "copy"; self.acodec = "copy"
		self.vbitrate = "copy"; self.abitrate = "copy"
		self.preset = "medium"; self.resolution = "copy"
		self.downmix = False
		self.volume = 100
		self.sub_size = 25; self.sub_color = "white"
		
	def get_ffmpeg(self): return "ffmpeg"
	def get_info(self, input):
		return ["-hide_banner", "-i", input]
	def get_args(self, input, output, srt, additional):
		full_cmd = self.get_info(input) + self.preset_and_resolution() + self.codec_and_bitrate() + [output]
		print(' '.join(full_cmd))
		return full_cmd
		
	def codec_and_bitrate(self):
		return self.get_vcodec() + self.get_vbitrate() + self.get_acodec() + self.get_abitrate()
	def get_vcodec(self): return ['-c:v', self.vcodec]
	def get_acodec(self): return ['-c:a', self.acodec]
	def get_vbitrate(self):
		if self.vbitrate == "copy": return []
		else: return ['-b:v', self.vbitrate, '-maxrate', self.vbitrate, '-bufsize', '500k']
	def get_abitrate(self):
		if self.abitrate == "copy": return []
		else: return ['-b:a', self.abitrate]
		
		
	def preset_and_resolution(self): return self.get_preset() + self.get_resolution()
	def get_preset(self): return ['-preset', self.preset]
	def get_resolution(self):
		if self.resolution == "copy": return []
		else: return ['-s', self.resolution]
		
		
	def volume_and_downmix(self):
		return []
	def get_downmix(self):
		if self.downmix is True: return ['-ac', '2']
		else: return []
	def get_volume(self):
		return []
		
		
	def get_subtitle(self):
		return ['-vf subtitles={}:force_style="FontSize={}"'.format(self.sub_path, self.sub_size)]


class Convert2(QMainWindow):

	def __init__(self):
		super(__class__, self).__init__()
		uic.loadUi("./convert2.ui", self)
		self.setWindowTitle("Convert2")
		self.command = CmdBuilder()
		self.path = QDir.currentPath()
		self.process = QProcess(self)
		self.process.setProcessChannelMode(QProcess.MergedChannels)
		self.connects()
		
	def connects(self):
		self.convertButton.clicked.connect(self.convert)
		self.process.readyRead.connect(self.print_output)
		self.selectInputButton.clicked.connect(self.select_input_file)
		self.sSelectButton.clicked.connect(self.select_srt_file)
		self.infoButton.clicked.connect(self.show_info)
		self.clearOutputButton.clicked.connect(lambda: self.output.clear())
		self.vCodecCombo.currentIndexChanged.connect(self.set_vcodec)
		self.aCodecCombo.currentIndexChanged.connect(self.set_acodec)
		self.aBitrateCombo.currentIndexChanged.connect(self.set_abitrate)
		self.vBitrateCombo.currentIndexChanged.connect(self.set_vbitrate)
		self.vPresetCombo.currentIndexChanged.connect(self.set_preset)
		self.resolutionCombo.currentIndexChanged.connect(self.set_resolution)
		
	def set_vcodec(self): self.command.vcodec = self.vCodecCombo.currentText()
	def set_acodec(self): self.command.acodec = self.aCodecCombo.currentText()
	def set_vbitrate(self): self.command.vbitrate = self.vBitrateCombo.currentText()
	def set_abitrate(self): self.command.abitrate = self.aBitrateCombo.currentText()
	def set_preset(self): self.command.preset = self.vPresetCombo.currentText()
	def set_resolution(self): self.command.resolution = self.resolutionCombo.currentText()
	
	@pyqtSlot()
	def convert(self):
		if self.check_files_are_selected():
			self.start(self.command.get_args(self.inputFile.text(), self.outputFile.text(), self.sFilePath.text(), self.additionalCmd.text()))
			
	@pyqtSlot()
	def show_info(self):
		if self.check_files_are_selected():
			self.start(self.command.get_info(self.inputFile.text()))
		
	def check_files_are_selected(self):
		return True
		
	def start(self, args):
		self.process.start(self.command.get_ffmpeg(), args)
		
	@pyqtSlot()
	def print_output(self):
		self.output.append(str(self.process.readAll(), 'latin-1'))
		
	@pyqtSlot()
	def select_input_file(self):
		filename = QFileDialog.getOpenFileName(self, "Choose File", self.path)
		if filename[0]:
			self.path = filename[0]; self.inputFile.setText(self.path); self.outputFile.setText(self.path)
			
	@pyqtSlot()
	def select_srt_file(self):
		filename = QFileDialog.getOpenFileName(self, "Choose Subtitle", self.path)
		if filename[0]:
			self.path = filename[0]; self.sFilePath.setText(self.path)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	c2 = Convert2()
	c2.show()
	sys.exit(app.exec_())
	