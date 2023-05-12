from moviepy.editor import *

# This file is dedicated for extracting audio and saving it to a particular file

def extract_audio(video_file_location, output_audio_location):
    clip =  VideoFileClip(video_file_location)
    clip.audio.write_audiofile(output_audio_location)

