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

# insert subtitle on the video
SUBTITLE = ""

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