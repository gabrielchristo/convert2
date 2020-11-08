"""

Convert2 Tool
by Gabriel Christo
10/2020

TODO:
	
	logica combobox (só muda se transcodar video ou audio)
	overwrite quit method event

"""

from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt, QDir, QProcess
from commandBuilder import *

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
	
		self.convertButton.clicked.connect(self.convert) # convert input file accord to selected options
		self.selectInputButton.clicked.connect(self.select_input_file) # select input file
		self.sSelectButton.clicked.connect(self.select_srt_file) # select subtitle file
		self.infoButton.clicked.connect(self.show_info) # show selected file info
		self.xboxButton.clicked.connect(self.show_xbox_info) # show xbox supported formats
		self.clearOutputButton.clicked.connect(lambda: self.output.clear()) # clear process output text
		self.process.readyRead.connect(self.print_output) # show last output from process
		self.killButton.clicked.connect(self.kill_process) # kills ffmpeg process
		self.crrtCmdButton.clicked.connect(self.show_current_cmd) # show current command accord to selected options
		self.cheatsheetButton.clicked.connect(self.show_cheatsheet) # show some ffmpeg commands useful information
		
		self.vCodecCombo.currentTextChanged.connect(self.command.set_video_codec) # set video codec
		self.vBitrateCombo.currentTextChanged.connect(self.command.set_video_bitrate) # set video bitrate
		self.vPresetCombo.currentTextChanged.connect(self.command.set_video_preset) # set video preset
		self.resolutionCombo.currentTextChanged.connect(self.command.set_video_resolution) # set video resolution
		
		self.aCodecCombo.currentTextChanged.connect(self.command.set_audio_codec) # set audio codec
		self.aBitrateCombo.currentTextChanged.connect(self.command.set_audio_bitrate) # set audio bitrate
		self.downmixCheckbox.stateChanged.connect(self.command.set_audio_downmix) # set audio downmix
		self.aVolumeSpinbox.valueChanged.connect(self.command.set_audio_volume) # set audio volume
		
		self.sCheckbox.stateChanged.connect(self.command.set_subtitle_insert) # set subtitle use
		self.subColorCombo.currentTextChanged.connect(self.command.set_subtitle_color) # set subtitle color
		self.subSizeSpinbox.valueChanged.connect(self.command.set_subtitle_size) # set subtitle size
	
	@pyqtSlot()
	def convert(self) -> None:
		if self.check_files_are_selected():
			self.start(self.command.get_convert_cmd(**(self.get_inputs_dict())))
			
	def get_inputs_dict(self) -> Dict:
		inputsDict = {'i': self.inputFile.text(), 'o': self.outputFile.text(), 's': self.sFilePath.text(), 'a': self.additionalCmd.text()}
		return inputsDict
		
	@pyqtSlot()
	def show_info(self) -> None:
		if self.check_files_are_selected():
			self.start(self.command.get_info_cmd(self.inputFile.text()))
		
	def check_files_are_selected(self) -> bool:
		# check needed files are selected
		return True
		
	def start(self, cmd: Tuple[str, List]) -> None:
		# start ffmpeg/ffprobe process with desired arguments
		self.process.start(cmd[0], cmd[1])
		
	@pyqtSlot()
	def kill_process(self) -> None:
		self.output.append("Process killed")
		self.process.kill()
		
	@pyqtSlot()
	def print_output(self) -> None:
		self.output.append(str(self.process.readAll(), 'latin-1'))
		
	@pyqtSlot()
	def select_input_file(self) -> None:
		filename = QFileDialog.getOpenFileName(self, "Choose File", self.path)
		if filename[0]:
			self.path = filename[0]; self.inputFile.setText(self.path); self.outputFile.setText(self.path)
			
	@pyqtSlot()
	def select_srt_file(self) -> None:
		filename = QFileDialog.getOpenFileName(self, "Choose Subtitle", self.path)
		if filename[0]:
			self.path = filename[0]; self.sFilePath.setText(self.path)
	
	@pyqtSlot()
	def show_xbox_info(self) -> None:
		self.show_message_box(XBOX_FORMATS, "Xbox Supported Formats")
		
	@pyqtSlot()
	def show_current_cmd(self) -> None:
		cmdTuple = self.command.get_convert_cmd(**(self.get_inputs_dict()))
		self.show_message_box(' '.join(cmdTuple[1]), "Current FFMPEG Command")
		
	@pyqtSlot()
	def show_cheatsheet(self) -> None:
		self.show_message_box(CHEATSHEET, "FFMPEG Cheatsheet")
	
	def show_message_box(self, text: str, title: str) -> None:
		msgBox = QMessageBox();
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText(text)
		msgBox.setWindowTitle(title)
		msgBox.setStandardButtons(QMessageBox.Ok)
		msgBox.exec()
		