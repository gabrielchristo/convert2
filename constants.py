DEBUG = True

# ffmpeg executable names
FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

# define codec for video stream
# receives the codec
VIDEO_CODEC = ["-c:v"]
# define bitrate for video stream
# receives the bitrate
VIDEO_BITRATE = ["-b:v"]
MAX_RATE = ["-maxrate"]
BUFSIZE = ["-bufsize", "1M"]
# define resolution of video
# receives scale
VIDEO_RESOLUTION = ["-s"]
# define video preset
# receives preset
VIDEO_PRESET = ["-preset:v"]
# burn subtitle into the video stream
# receives subtitle file path (utf8), font size, font color (BGR)
VIDEO_FILTER = ["-filter:v"]
INSERT_SUBTITLE_LABEL = "subtitles={}:force_style='FontSize={},PrimaryColour=&H{}&'"
SUBTITLE_WHITE = "FFFFFF"
SUBTITLE_YELLOW = "00FFFF"

# define codec for audio stream
# receives the desired codec
AUDIO_CODEC = ["-c:a"]
AAC_OPTION = ["-aac_coder", "fast"]
# define bitrate for audio stream
# receives the desired bitrate
AUDIO_BITRATE = ["-b:a"]
# define downmix of audio stream to 2 channels
AUDIO_DOWNMIX = ['-ac', '2']
# define volume of audio stream
AUDIO_FILTER = ["-filter:a"]
AUDIO_VOLUME_LABEL = "volume={}"

# hide ffmpeg banner
HIDE_BANNER = ["-hide_banner"]
# define input file
INPUT = ["-i"]

# show file information
# receives file name/path
FILEINFO = HIDE_BANNER + ["-v", "quiet", "-print_format", "json", "-show_format", "-show_streams"]

# default values to all ffmpeg commands
# -threads 0 tells to ffmpeg optimize the cpu and cores use
# -movflags and +faststart allows to playback the media without have completed the download/conversion
DEFAULT = ["-threads", "0", "-movflags", "+faststart"]

XBOX_FORMATS = """AVI: Video Simple/Advanced 5Mbps 1280x720@30 | Audio Dolby 2ch/5.1ch or MP3\n
WMV: Video WMV7,8,9/VC1 Simple/Advanced/Main/High3 15Mbps 1920x1080@30 | Audio WMA 7,8,9 Pro,Lossless\n
H.264: Video Baseline/Main/High4.1 10Mbps 1920x1080@30 | Audio AAC LC 2ch\n
MPEG-4: Video Simple/Advanced 5Mbps 1280x720@30 | Audio AAC LC 2ch"""

CHEATSHEET = """
<h3>Streams</h3>
<p>-map 0:1 means stream 1 from first input file</p>
<p>-map 1:0 means stream 0 from second input file</p>
<h3>Delay Audio and Video</h3>
<p>-i input.mp4 -i input.mp4 -itsoffset 3.84 (seconds) -map 0:v -map 1:a</p>
<h3>Delay Subtitle</h3>
<p>-i sub.srt -itsoffset 2.5 -c copy sub_out.srt</p>
<h3>Trim Video</h3>
<p>-ss 00:00:10 -to 00:00:20</p>
<h3>Crop Video</h3>
<p>-filter:v "crop=width:height:x:y"</p>
<p>x, y: starting position and width, height: rectangle size</p>
<h3>x264 Profiles</h3>
<p>-profile:v [main, high, baseline]</p>
<p>-level:v [4.0, 4.1, ...]</p>
<h3>Remove Streams</h3>
<p>-[a, s, v]n</p>
"""


