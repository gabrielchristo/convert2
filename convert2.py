"""

Convert2 Tool
by Gabriel Christo
10/2020

TODO:
		
	overwrite quit method event (check process still running)
	video fps
	video bitrate lineedit and unit combobox
	downmix to mono (radio button)
	style scrollbar
	check file exists before start
	save log button (with config)

"""

from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt, QDir, QProcess
from PyQt5.QtGui import QColor, QIcon, QPixmap
from commandBuilder import *
from scrollablePopup import *

from bitrateCalculator import *
from datetime import datetime

class Convert2(QMainWindow):

	def __init__(self):
		super(__class__, self).__init__()
		uic.loadUi("./convert2.ui", self)
		self.setWindowTitle("Convert2")
		self.setWindowIcon(QIcon(ICON))
		self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
		self.nameLabel.setVisible(True)
		self.command = CmdBuilder()
		self.path = QDir.currentPath()
		self.process = QProcess(self)
		self.process.setProcessChannelMode(QProcess.MergedChannels)
		self.popup = scrollablePopup()
		self.connects()
		self.ledLabel.setPixmap(QPixmap(RED_LED).scaledToHeight(LED_HEIGHT))
		self.bitCalculator = BitrateCalculator()
		
	def connects(self):
	
		self.convertButton.clicked.connect(self.convert) # convert input file according to selected options
		self.selectInputButton.clicked.connect(self.select_input_file) # select input file
		self.outFileButton.clicked.connect(self.select_output_file) # select output file
		self.sSelectButton.clicked.connect(self.select_srt_file) # select subtitle file
		self.infoButton.clicked.connect(self.show_info) # show selected file info
		self.clearOutputButton.clicked.connect(lambda: self.output.clear()) # clear process output text
		self.process.readyRead.connect(self.print_output) # show last output from process
		self.process.started.connect(self.process_started) # set green led and updates label when starting process
		self.process.finished.connect(self.process_finished) # set red led and updates label when process is finished
		self.killButton.clicked.connect(self.kill_process) # kills ffmpeg process
		self.crrtCmdButton.clicked.connect(self.show_current_cmd) # show current command according to selected options
		self.cheatsheetButton.clicked.connect(self.show_cheatsheet) # show some ffmpeg commands useful information
		self.bitCalcButton.clicked.connect(self.show_bitrate_calculator) # show bitrate calculator window
		
		self.vCodecCombo.currentTextChanged.connect(self.command.set_video_codec) # set video codec
		self.vCodecCombo.currentTextChanged.connect(self.toggle_video_options) # enable/disable video options
		self.vBitrateCombo.currentTextChanged.connect(self.command.set_video_bitrate) # set video bitrate
		self.vPresetCombo.currentTextChanged.connect(self.command.set_video_preset) # set video preset
		self.resolutionCombo.currentTextChanged.connect(self.command.set_video_resolution) # set video resolution
		
		self.aCodecCombo.currentTextChanged.connect(self.command.set_audio_codec) # set audio codec
		self.aCodecCombo.currentTextChanged.connect(self.toggle_audio_options) # enable/disable audio options
		self.aBitrateCombo.currentTextChanged.connect(self.command.set_audio_bitrate) # set audio bitrate
		self.downmixCheckbox.stateChanged.connect(self.command.set_audio_downmix) # set audio downmix
		self.aVolumeSpinbox.valueChanged.connect(self.command.set_audio_volume) # set audio volume
		self.aRateCombobox.currentTextChanged.connect(self.command.set_audio_rate) # set audio sample rate frequency
		
		self.sCheckbox.stateChanged.connect(self.command.set_subtitle_insert) # set subtitle use
		self.sCheckbox.stateChanged.connect(self.toggle_subtitle_options) # enable/disable subtitle options
		self.sCheckbox.stateChanged.connect(self.show_subtitle_encoding_warning) # show subtitle char encoding warning
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
		if(self.inputFile.text() == ""):
			self.show_message_box("Choose a input file", "No file selected"); return False
		elif(self.sCheckbox.isChecked() and self.sFilePath.text() == ""):
			self.show_message_box("Choose a subtitle file", "No file selected"); return False
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
		now = datetime.now().strftime("%d/%m/%Y %H:%M:%S -> ")
		self.output.append(now + str(self.process.readAll(), 'latin-1'))
		
	@pyqtSlot()
	def select_input_file(self) -> None:
		filename = QFileDialog.getOpenFileName(self, "Choose File", self.path, FILE_CONTAINERS)
		if filename[0]:
			self.path = filename[0]; self.inputFile.setText(self.path)
			
	@pyqtSlot()
	def select_output_file(self) -> None:
		filename = QFileDialog.getSaveFileName(self, "Choose File", self.path, FILE_CONTAINERS)
		if filename[0]:
			self.outputFile.setText(filename[0])
			
	@pyqtSlot()
	def select_srt_file(self) -> None:
		filename = QFileDialog.getOpenFileName(self, "Choose Subtitle", self.path)
		if filename[0]:
			self.path = filename[0]; self.sFilePath.setText(self.path)
		
	@pyqtSlot()
	def show_current_cmd(self) -> None:
		if self.check_files_are_selected():
			cmdTuple = self.command.get_convert_cmd(**(self.get_inputs_dict()))
			self.show_message_box(' '.join([cmdTuple[0]] + cmdTuple[1]), "Current FFMPEG Command")
		
	@pyqtSlot()
	def show_cheatsheet(self) -> None:
		self.popup.setText(CHEATSHEET + XBOX_FORMATS)
		self.popup.setTitle("FFMPEG Cheatsheet")
		self.popup.setWindowIcon(QIcon(ICON))
		self.popup.show()
	
	@pyqtSlot()
	def show_bitrate_calculator(self) -> None:
		self.bitCalculator.show()
		
	def show_message_box(self, text: str, title: str) -> None:
		msgBox = QMessageBox();
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText(text)
		msgBox.setWindowTitle(title)
		msgBox.setWindowIcon(QIcon(ICON))
		msgBox.setStandardButtons(QMessageBox.Ok)
		msgBox.exec()
		
	@pyqtSlot(int)
	def show_subtitle_encoding_warning(self, checkboxState: int) -> None:
		if checkboxState != 0: self.show_message_box(SUBTITLE_ENCODING, "Char Encoding")
		
	@pyqtSlot(str)
	def toggle_video_options(self, crrtText: str) -> None:
		bool = False if crrtText == COPY else True
		self.vBitrateCombo.setEnabled(bool)
		self.vPresetCombo.setEnabled(bool)
		self.resolutionCombo.setEnabled(bool)
		# subtitle logic below
		self.sCheckbox.setEnabled(bool)
		self.toggle_subtitle_options(bool and self.sCheckbox.isChecked())
		
	@pyqtSlot(str)
	def toggle_audio_options(self, crrtText: str) -> None:
		bool = False if crrtText == COPY else True
		self.aBitrateCombo.setEnabled(bool)
		self.aVolumeSpinbox.setEnabled(bool)
		self.downmixCheckbox.setEnabled(bool)
		self.aRateCombobox.setEnabled(bool)
	
	@pyqtSlot(int)
	def toggle_subtitle_options(self, crrtState: int) -> None:
		bool = False if crrtState == 0 else True
		self.sFilePath.setEnabled(bool)
		self.subColorCombo.setEnabled(bool)
		self.subSizeSpinbox.setEnabled(bool)
		self.sSelectButton.setEnabled(bool)
		
	@pyqtSlot()	
	def process_started(self) -> None:
		if DEBUG: print(RUNNING)
		self.processStatusLabel.setText(RUNNING)
		self.ledLabel.setPixmap(QPixmap(GREEN_LED).scaledToHeight(LED_HEIGHT))
		
	@pyqtSlot()
	def process_finished(self) -> None:
		if DEBUG: print(NOT_RUNNING)
		self.processStatusLabel.setText(NOT_RUNNING)
		self.ledLabel.setPixmap(QPixmap(RED_LED).scaledToHeight(LED_HEIGHT))
		