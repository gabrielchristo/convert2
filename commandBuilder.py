
from typing import Tuple, List, Dict
from PyQt5.QtCore import pyqtSlot, QObject
from constants import *
import platform

class CmdBuilder(QObject):
	
	def __init__(self):
		super(__class__, self).__init__()
	
		self.vcodec = COPY
		self.vbitrate = COPY
		self.vpreset = "medium"
		self.vresolution = COPY
		
		self.acodec = COPY
		self.abitrate = COPY
		self.adownmix = False
		self.avolume = 100
		self.arate = COPY
		
		self.sinsert = False
		self.ssize = 25
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
		if self.abitrate == COPY or self.acodec == COPY: return []
		else: return AUDIO_BITRATE + [self.abitrate]
		
	def get_video_bitrate_cmd(self) -> List[str]:
		if self.vbitrate == COPY or self.vcodec == COPY: return []
		else:
			vbit = [self.vbitrate]
			return VIDEO_BITRATE + vbit + MAX_RATE + vbit + BUFSIZE + vbit
		
	def get_audio_codec_cmd(self) -> List[str]:
		return AUDIO_CODEC + [self.acodec]
		
	def get_video_resolution_cmd(self) -> List[str]:
		if self.vresolution == COPY or self.vcodec == COPY: return []
		else: return VIDEO_RESOLUTION + [self.vresolution]
		
	def get_video_preset_cmd(self) -> List[str]:
		if self.vpreset == "medium" or self.vcodec == COPY: return []
		else: return VIDEO_PRESET + [self.vpreset]
		
	def get_audio_downmix_cmd(self) -> List[str]:
		if self.adownmix is True and self.acodec != COPY: return AUDIO_DOWNMIX
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
		cmd += self.get_audio_rate_cmd()
		cmd += self.get_audio_downmix_cmd()
		cmd += self.get_audio_volume_cmd()
		additional = kwargs.get('a')
		if(len(additional) > 0): cmd += additional.split()
		cmd += DEFAULT
		cmd += [kwargs.get('o')]
		if DEBUG: print(' '.join(cmd))
		return FFMPEG, cmd
		
		
	def get_audio_volume_cmd(self) -> List[str]:
		if self.avolume == 100 or self.acodec == COPY: return []
		else: return AUDIO_FILTER + [AUDIO_VOLUME_LABEL.format(self.avolume/100)]
		
	@pyqtSlot(int)
	def set_audio_volume(self, volume: int) -> None:
		if DEBUG: print(volume)
		self.avolume = volume
		
	
	def get_subtitle_cmd(self, subtitle: str) -> List[str]:
		color = (SUBTITLE_WHITE if self.scolor == "white" else SUBTITLE_YELLOW)

		if platform.system() == "Linux": corrected_path = subtitle # no changes to subtitle path at linux os
		elif platform.system() == "Windows": corrected_path = subtitle.replace('/', '\\\\\\\\').replace(':', '\\\\:') # fix windows bug with ffmpeg path chars escaping

		if self.sinsert is False or self.vcodec == COPY: return []
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
		
	@pyqtSlot(str)
	def set_audio_rate(self, rate: str) -> None:
		if DEBUG: print(rate)
		self.arate = rate
		
	def get_audio_rate_cmd(self) -> List[str]:
		if self.arate == COPY or self.acodec == COPY: return []
		else: return AUDIO_RATE + [self.arate]
		