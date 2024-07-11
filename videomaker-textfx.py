from moviepy.editor import *
from moviepy.video.tools.drawing import color_gradient
import os
from PIL import Image
import numpy as np
import random

# Set the path to the ImageMagick binary
os.environ['IMAGEMAGICK_BINARY'] = '/usr/local/bin/magick'

# Function to clean up the path
def clean_path(path):
    return path.strip().strip("'").strip('"')

# Custom resize function
def custom_resize(image_clip, height):
    def resize_image(image):
        pil_image = Image.fromarray(image)
        new_width = int(pil_image.width * (height / pil_image.height))
        resized_pil_image = pil_image.resize((new_width, height), Image.Resampling.LANCZOS)
        return np.array(resized_pil_image)
    
    return image_clip.fl_image(resize_image)

# Animation #1: Wave effect
def wave_effect(txt_clip):
    def wave_text(t):
        scale = 1 + 0.2 * np.sin(2 * np.pi * t)
        return txt_clip.resize(scale)
    return txt_clip.fl_time(wave_text)

# Animation #2: Accordion effect
def accordion_effect(txt_clip):
    def accordion_text(t):
        return txt_clip.resize(lambda t: 1 + 0.2 * np.sin(2 * np.pi * t))
    return txt_clip.fl_time(accordion_text)

# Animation #3: Opacity effect
def opacity_effect(txt_clip):
    def opacity_text(t):
        opacity = 0.5 + 0.5 * np.sin(2 * np.pi * t)
        return txt_clip.set_opacity(opacity)
    return txt_clip.fl_time(opacity_text)

# Animation #4: Elastic effect
def elastic_effect(txt_clip):
    def elastic_text(t):
        scale = 1 + 0.05 * np.sin(2 * np.pi * t / 2)
        return txt_clip.resize(scale)
    return txt_clip.fl_time(elastic_text)

# Function to get user inputs
def get_inputs():
    image_path = input("Enter the path to the image (jpg): ").strip()
    audio_path = input("Enter the path to the audio file (mp3): ").strip()
    video_title = input("Enter the video title: ").strip()
    return clean_path(image_path), clean_path(audio_path), video_title

# Function to create the video
def create_video(image_path, audio_path, video_title):
    try:
        # Load image and audio
        image_clip = ImageClip(image_path)
        audio_clip = AudioFileClip(audio_path)
        
        # Debugging: Print audio properties
        print(f"Audio duration: {audio_clip.duration} seconds")
        print(f"Audio fps: {audio_clip.fps}")
        
        # Set the duration of the image clip to match the audio clip
        image_clip = image_clip.set_duration(audio_clip.duration)
        
        # Resize the image to fit the video
        image_clip = custom_resize(image_clip, height=720)
        
        # Create a text clip with Times New Roman font and black color
        txt_clip = TextClip(
            video_title,
            fontsize=70,
            color='black',
            font='Times-New-Roman',
            align='center'
        ).set_position('center').set_duration(audio_clip.duration)
        
        # Define the animations
        animations = [wave_effect, accordion_effect, opacity_effect, elastic_effect]
        random.shuffle(animations)
        
        # Apply the animations with gaps
        total_duration = audio_clip.duration
        animation_duration = random.uniform(5, 15)
        gap_duration = 60
        current_time = 0
        txt_clips = []

        while current_time + animation_duration < total_duration:
            for animation in animations:
                anim_clip = animation(txt_clip).set_start(current_time).set_duration(animation_duration)
                txt_clips.append(anim_clip)
                current_time += animation_duration + gap_duration
                if current_time + animation_duration > total_duration:
                    break

        # Composite the final video
        video = CompositeVideoClip([image_clip] + txt_clips)
        
        # Set the audio
        video = video.set_audio(audio_clip)
        
        # Write the result to a file
        output_path = "output_video.mp4"
        video.write_videofile(output_path, fps=24, audio_codec='aac')
    
        print(f"Video saved as {output_path}")
    
    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    image_path, audio_path, video_title = get_inputs()
    create_video(image_path, audio_path, video_title)
