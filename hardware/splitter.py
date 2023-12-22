"""
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

def split_video_into_fragments(fragment_duration):
    input_video_file = "Default_user.avi"
    output_folder = "/content/video_fragments/"
    os.makedirs(output_folder, exist_ok=True)
    clip = VideoFileClip(input_video_file)
    duration = int(clip.duration)
    
    fragment_start = 0
    fragment_end = fragment_duration
    
    fragment_num = 1
    
    while fragment_end <= duration:
        output_file = os.path.join(output_folder, f"fragment_{fragment_num}.mp4")
        ffmpeg_extract_subclip(input_video_file, fragment_start, fragment_end, targetname=output_file)
        
        fragment_start += fragment_duration
        fragment_end += fragment_duration
        fragment_num += 1

split_video_into_fragments(5)
"""
