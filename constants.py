DEBUG = True

COPY = "copy"
ICON = "./icon.png"
LED_HEIGHT = 23
GREEN_LED = "./green_led.png"
RED_LED = "./red_led.png"
RUNNING = "Process is running"
NOT_RUNNING = "Process is not running"
SUBTITLE_ENCODING = "Make sure you have a valid UTF-8 encoded SRT file"
FILE_CONTAINERS = "Media Files (*.mkv *.mp4 *.3gp *.avi *.wmv *.flv *.ts *.mpg *.mov *.rmvb *.vob *.webm)"

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
BUFSIZE = ["-bufsize"] # removed "1M" buffer 29/12/2020
# define resolution of video
# receives scale
VIDEO_RESOLUTION = ["-s"]
# define video preset
# receives preset
VIDEO_PRESET = ["-preset:v"]
# burn subtitle into the video stream
# receives subtitle file path (utf8), font size, font color (BGR)
VIDEO_FILTER = ["-filter:v"]
INSERT_SUBTITLE_LABEL = "subtitles={}:force_style=\'FontSize={},PrimaryColour=&H{},Bold=1,Shadow=1\'"
SUBTITLE_WHITE = "FFFFFF"
SUBTITLE_YELLOW = "00FFFF"

# define codec for audio stream
# receives the desired codec
AUDIO_CODEC = ["-c:a"]
AAC_OPTION = ["-aac_coder", "fast"] # not being used
# define bitrate for audio stream
# receives the desired bitrate
AUDIO_BITRATE = ["-b:a"]
# define downmix of audio stream to 2 channels
AUDIO_DOWNMIX = ['-ac', '2']
# define volume of audio stream
AUDIO_FILTER = ["-filter:a"]
AUDIO_VOLUME_LABEL = "volume={}"
# defines audio sample rate
# receives desired frequency in Hz
AUDIO_RATE = ["-ar"]

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
DEFAULT = ["-threads", "0"] # removed "-movflags", "+faststart" moov atom options 30/12/2020

XBOX_FORMATS = """<h4>Xbox 360 Supported Formats</h4>
<p>AVI: Video Simple/Advanced 5Mbps 1280x720@30 | Audio Dolby 2ch/5.1ch or MP3</p>
<p>WMV: Video WMV7,8,9/VC1 Simple/Advanced/Main/High3 15Mbps 1920x1080@30 | Audio WMA 7,8,9</p>
<p>H.264: Video Baseline/Main/High4.1 10Mbps 1920x1080@30 | Audio AAC LC 2ch</p>
<p>MPEG-4: Video Simple/Advanced 5Mbps 1280x720@30 | Audio AAC LC 2ch</p>"""

CHEATSHEET = """
<h4>Streams</h4>
<p>-map 0:1 means stream 1 from first input file</p>
<p>-map 1:0 means stream 0 from second input file</p>

<h4>Delay Audio and Video</h4>
<p>-i input.mp4 -i input.mp4 -itsoffset 3.84 (seconds) -map 0:v -map 1:a</p>

<h4>Delay Subtitle</h4>
<p>-i sub.srt -itsoffset 2.5 -c copy sub_out.srt</p>

<h4>Trim Video</h4>
<p>-ss 00:00:10 -to 00:00:20</p>

<h4>Crop Video</h4>
<p>-filter:v "crop=width:height:x:y"</p>
<p>x, y: starting position and width, height: rectangle size</p>

<h4>libx264 Profiles</h4>
<p>-profile:v [main, high, high10, high422, high444, baseline]</p>

<h4>libx264 Levels</h4>
<p>-level:v desiredLevel</p>
<p>3 - maximum 720x480@30</p>
<p>3.1 - maximum HD@30</p>
<p>4 and 4.1 - maximum FHD@30 or 2048x1024@30</p>
<p>5 and 5.1 - maximum 2K@30 or 4K@30</p>

<h4>Pixel Format</h4>
<p>-pix_fmt desiredFormat</p>
<p>yuv420p - 6 bytes per 4 pixels reordered. Full compatibility</p>
<p>yuv422 - 8 bytes per 4 pixels</p>
<p>yuv444 - 12 bytes per 4 pixels</p>
<p>rgb24</p>
<p>bgr24</p>
<p>gray</p>
<p>pal8</p>

<h4>Remove Streams</h4>
<p>-[a, s, v]n</p>

<h4>Dynamic Range Compression</h4>
<p>Get the audio volume info:</p>
<p>-af volumedetect -vn null</p>
<p>To apply the filter:</p>
<p>-filter_complex "compand=attacks=0:points=-40/-10|-1/10|0/0:gain=3"</p>
<p>Generate wave form image:</p>
<p>-filter_complex showwavespic -frames:v 1</p>

<h4>Normalize Audio</h4>
<p>I:target loudness in LUFs LRA:loudness range TP:true peak</p>
<p>-af loudnorm=I=-23:LRA=7:tp=-2</p>

<h4>Solve "Too many packets buffered" problem</h4>
<p>-max_muxing_queue_size 1024</p>

<h4>Resolution Guide</h4>
<p>hd2160 - 3840x2160</p>
<p>hd1440 - 2560x1440</p>
<p>hd1080 - 1920x1080</p>
<p>hd720 - 1280x720</p>
<p>hd480 - 854x480</p>
<p>vga - 640x480</p>
<p>hd360 - 640x360</p>
<p>qvga - 320x240</p>
<p>qqvga - 160x120</p>

<h4>Remove Metadata</h4>
<p>-map_metadata -1</p>
<p>-map_chapters -1</p>
"""
