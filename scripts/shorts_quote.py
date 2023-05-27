# Import everything needed to edit video clips
from moviepy.editor import *
from moviepy.video.fx.all import crop
import glob
import random
from helper.aspectratio import calculate_aspect

# Search all video files inside a specific folder
dir_path = r'./data/videos/cars/*.*'
clipPaths = glob.glob(dir_path)
randomClip = random.choice(clipPaths)

# Parametrize Video generation
first_quote_length =    9
pause_length =          1   
second_quote_length =   1.5
total_length =          first_quote_length + pause_length + second_quote_length

output_width =          1080
output_height =         1920

# DEBUG
headline_text =      "Another Awesome Channel"
first_quote_text =   "Lorem Ipsum"
second_quote_text =  "dolor sir amit"
copyright_text =     "@anotherawesomechannel"

(input_width, input_height) = VideoFileClip(randomClip).size
input_aspect_ratio = calculate_aspect(input_width, input_height)
output_aspect_ratio = calculate_aspect(output_width, output_height)
    
print("Input video width: " + str(input_width))
print("Input video height: " + str(input_height))
print("Input video aspect ratio: " + str(input_aspect_ratio))

print("Output video width: " + str(output_width))
print("Output video height: " + str(output_height))
print("Output video aspect ratio: " +str(output_aspect_ratio))

background_video = VideoFileClip(randomClip,audio=False)
if input_aspect_ratio != output_aspect_ratio:
    print(background_video.size)
    background_video = background_video.resize(height=output_height)

background_video_cropped = crop(background_video, width=output_width, height=output_height, x_center=background_video.size[0]/2, y_center=background_video.size[1]/2)

# Generate Text
headline = TextClip(headline_text,fontsize=64,color='white',font='Garet-Book',kerning=0)
headline = headline.set_pos(("center",350))

first_quote = TextClip(first_quote_text,fontsize=48,color='white',font='Garet-Heavy')
first_quote = first_quote.set_pos(("center","center"))
first_quote = first_quote.set_end(first_quote_length)


second_quote = TextClip(second_quote_text,fontsize=48,color='white',font='Garet-Book')
second_quote = second_quote.set_pos(("center","center"))
second_quote = second_quote.set_start(first_quote_length + pause_length)

copyright = TextClip(second_quote_text,fontsize=32,color='white',font='Garet-Book')
copyright = copyright.set_pos(("center",1700))

final_video = CompositeVideoClip([background_video_cropped,headline,first_quote,second_quote,copyright]).subclip(0,total_length)

final_video.write_videofile(filename="./output/test_shorts.mp4",fps=25,audio=True,threads=8)