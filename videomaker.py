from moviepy.editor import *
from moviepy.video.tools.drawing import color_gradient
import os
from PIL import Image
import numpy as np

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
        )
        
        # Animate the text
        def move_text(t):
            return 'center', 50 + 10 * t
        
        txt_clip = txt_clip.set_position(move_text).set_duration(audio_clip.duration).set_opacity(0.8)
        
        # Composite the final video
        video = CompositeVideoClip([image_clip, txt_clip])
        
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
