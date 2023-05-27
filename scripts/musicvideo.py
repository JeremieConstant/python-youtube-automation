# Import everything needed to edit video clips
from moviepy.editor import *
import glob
import random
import math

# Search all video files inside a specific folder
# *.* means file name with any extension
dir_path = r'./data/videos/cars/*.*'
clipPaths = glob.glob(dir_path)
random.shuffle(clipPaths)

print("Found " + str(len(clipPaths)) + " videos")

# Parametrize Video generation
clipLength = 2.5
music = AudioFileClip('./data/music/Emin Nilsen - Champion Of Death.mp3').subclip(0,10)
print("Song is " + str(music.duration) + " seconds long")

artistTitle  = 'Emin Nilsen'
trackTitle   = 'Champions of Death'

# Use only as much clips as needed
necessaryVideosAmount = math.ceil(music.duration / clipLength)
print("Attempting to load " + str(necessaryVideosAmount) + " clips for the video")


# Load all clips from the folder.
clips = [VideoFileClip(n, audio=False, target_resolution=[1080,1920]).subclip(0,clipLength) for n in clipPaths[:necessaryVideosAmount]]
print(str(len(clips)) + " clips successfully loaded")


# Generate Text
header = TextClip("BUSINESSES OF TOMORROW",fontsize=18,color='white',font='Garet-Book',kerning=8)
header = header.set_pos(("center",120))
print('Header successfully generated')

artist = TextClip(artistTitle,fontsize=19,color='white',font='Garet-Heavy')
artist = artist.set_pos((690,750))
print('Artist successfully generated')

track = TextClip(trackTitle,fontsize=19,color='white',font='Garet-Book')
track = track.set_pos((690,785))
print('Track successfully generated')

# Load Cover Art
art = ImageClip('./data/art/1.jpg')
art = art.set_pos((690,187))
art = art.resize((538,538))
print('Cover art successfully located')

# Overlay the text clip on the first video clip
video = concatenate_videoclips(clips)
video.audio = music

# START: Progressbar

progressbar_width = 538
progressbar_height = 3

# Step 3: Create a color clip to serve as the mask
# progressbar_inactive_color = (169, 175, 198)
# progressbar_active_color = (255, 255, 255)

progressbar_inactive_color = (255, 0, 0)
progressbar_active_color = (0, 0, 255)

progressbar_active = ColorClip(size=(progressbar_width, progressbar_height), col=progressbar_active_color)
progressbar_inactive = ColorClip(size=(progressbar_width, progressbar_height), col=progressbar_inactive_color)

# Step 4: Position the mask within the video frame
progressbar_position = (690, 852)  # Adjust the position as needed

progressbar_inactive = progressbar_inactive.set_position(progressbar_position).set_duration(video.duration)
progressbar_active = progressbar_active.set_position(progressbar_position).set_duration(video.duration)

#END: Progressbar

for clip in clips:
    clip.close()

final_video = CompositeVideoClip([video,header,artist,track,txt_clip]).subclip(0,music.duration)



# Write the result to a file (many options available !)
final_video.write_videofile(filename="./output/test_multiple.mp4",fps=25,audio=True,threads=8)