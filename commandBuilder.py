
from typing import Tuple, List, Dict
from PyQt5.QtCore import pyqtSlot, QObject
from constants import *

class CmdBuilder(QObject):
	
	def __init__(self):
		super(__class__, self).__init__()
	
		self.vcodec = "copy"
		self.vbitrate = "copy"
		self.vpreset = "medium"
		self.vresolution = "copy"
		
		self.acodec = "copy"
		self.abitrate = "copy"
		self.adownmix = False
		self.avolume = 100
		
		self.sinsert = False
		self.ssize = 25;
		self.scolor = "white"
		
	@pyqtSlot(str)
	def set_video_codec(self, codec: str) -> None:
		if DEBUG: print(codec)
		self.vcodec = codec
		
	@pyqtSlot(str)
	def set_video_bitrate(self, bitrate: str) -> None:
		if DEBUG: print(bitrate)
		self.vbitrate = bitrate
		
	@pyqtSlot(str)
	def set_audio_codec(self, codec: str) -> None:
		if DEBUG: print(codec)
		self.acodec = codec
		
	@pyqtSlot(str)
	def set_audio_bitrate(self, bitrate: str) -> None:
		if DEBUG: print(bitrate)
		self.abitrate = bitrate
		
	@pyqtSlot(str)
	def set_video_resolution(self, resolution: str) -> None:
		if DEBUG: print(resolution)
		self.vresolution = resolution
		
	@pyqtSlot(str)
	def set_video_preset(self, preset: str) -> None:
		if DEBUG: print(preset)
		self.vpreset = preset
		
	@pyqtSlot(int)
	def set_audio_downmix(self, checked: int) -> None:
		if DEBUG: print(checked)
		self.adownmix = (False if checked == 0 else True)
		
	def get_info_cmd(self, input: str) -> Tuple[str, List]:
		if DEBUG: print(FFPROBE, FILEINFO, input)
		return FFPROBE, FILEINFO + [input]
		
	def get_video_codec_cmd(self) -> List[str]:
		return VIDEO_CODEC + [self.vcodec]
		
	def get_audio_bitrate_cmd(self) -> List[str]:
		if self.abitrate == "copy": return []
		else: return AUDIO_BITRATE + [self.abitrate]
		
	def get_video_bitrate_cmd(self) -> List[str]:
		if self.vbitrate == "copy": return []
		else: return VIDEO_BITRATE + [self.vbitrate] + MAX_RATE + [self.vbitrate] + BUFSIZE
		
	def get_audio_codec_cmd(self) -> List[str]:
		return AUDIO_CODEC + [self.acodec] + (AAC_OPTION if self.acodec == "aac" else [])
		
	def get_video_resolution_cmd(self) -> List[str]:
		if self.vresolution == "copy": return []
		else: return VIDEO_RESOLUTION + [self.vresolution]
		
	def get_video_preset_cmd(self) -> List[str]:
		if self.vpreset == "medium": return []
		else: return VIDEO_PRESET + [self.vpreset]
		
	def get_audio_downmix_cmd(self) -> List[str]:
		if self.adownmix is True: return AUDIO_DOWNMIX
		else: return []
		
	def get_convert_cmd(self, **kwargs) -> Tuple[str, List]:
		# return the full conversion command based on received args and gui
		# i:input o:output s:subtitle a:additional
		cmd = HIDE_BANNER + INPUT + [kwargs.get('i')]
		cmd += self.get_video_preset_cmd()
		cmd += self.get_video_resolution_cmd()
		cmd += self.get_video_codec_cmd()
		cmd += self.get_video_bitrate_cmd()
		cmd += self.get_subtitle_cmd(kwargs.get('s'))
		cmd += self.get_audio_codec_cmd()
		cmd += self.get_audio_bitrate_cmd()
		cmd += self.get_audio_downmix_cmd()
		cmd += self.get_audio_volume_cmd()
		cmd += DEFAULT
		additional = kwargs.get('a')
		if(len(additional) > 0): cmd += [additional]
		cmd += [kwargs.get('o')]
		if DEBUG: print(' '.join(cmd))
		return FFMPEG, cmd
		
		
	def get_audio_volume_cmd(self) -> List[str]:
		if self.avolume == 100: return []
		else: return AUDIO_FILTER + [AUDIO_VOLUME_LABEL.format(self.avolume/100)]
		
	@pyqtSlot(int)
	def set_audio_volume(self, volume: int) -> None:
		if DEBUG: print(volume)
		self.avolume = volume
		
	
	def get_subtitle_cmd(self, subtitle: str) -> List[str]:
		color = (SUBTITLE_WHITE if self.scolor == "white" else SUBTITLE_YELLOW)
		corrected_path = subtitle.replace('/', '\\\\\\\\').replace(':', '\\\\:') # bug with ffmpeg path chars escaping
		if self.sinsert is False: return []
		else: return VIDEO_FILTER + [INSERT_SUBTITLE_LABEL.format(corrected_path, self.ssize, color)]
	

	@pyqtSlot(str)
	def set_subtitle_color(self, color: str) -> None:
		if DEBUG: print(color)
		self.scolor = color
		
	@pyqtSlot(int)
	def set_subtitle_size(self, size: int) -> None:
		if DEBUG: print(size)
		self.ssize = size

	@pyqtSlot(int)
	def set_subtitle_insert(self, insert: int) -> None:
		if DEBUG: print(insert)
		self.sinsert = (False if insert == 0 else True)

		