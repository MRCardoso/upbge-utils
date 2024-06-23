import subprocess
import os
import sys
import re
import cv2
import ffmpeg
import shutil
import mdxutils
"""
Thrid Part Libs
- ffmpeg
- cv2
"""
resolutions = [
    (3840, 2160),  # 4K
    (2560, 1440),  # 2K
    (1920, 1080),  # Full HD
]
extra_resolution = (
    '4K',
    '2K',
    'full-HD',
)

def print_progress_bar(percentage):
    bar_length = 50
    filled_length = int(bar_length * percentage / 100)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\r[{bar}] {percentage:.2f}%')
    sys.stdout.flush()

def extract_audio(input_video_path, audio_output_path):
    """
    Extract audio from the input video and save it as a separate audio file.
    """
    ffmpeg.input(input_video_path)\
    .audio\
    .filter('aformat', sample_fmts='s16')\
    .output(audio_output_path, format='mp3')\
    .run()

def combine_video_audio(input_path, audio_input_path, output_path):
    """
    Combine the upscaled video with the original audio.
    """
    input_video = ffmpeg.input(input_path)
    input_audio = ffmpeg.input(audio_input_path)
    ffmpeg.output(input_video, input_audio, output_path, vcodec='copy', acodec='aac', strict='experimental').run()

def upscale_video(input_path, temp_file, ext, index=0):
    
    input_path = os.path.abspath(input_path)
    cap = cv2.VideoCapture(input_path)
    # original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    frame_number = 0
    
    if ext == 'mkv':
        fourcc = cv2.VideoWriter_fourcc(*'X264')
        print('gen mkv')
    else:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_file, fourcc, fps, resolutions[index])
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, resolutions[index], interpolation=cv2.INTER_CUBIC)
        out.write(resized_frame)
        frame_number += 1
        percentage = (frame_number / frame_count) * 100
        print_progress_bar(percentage)
    cap.release()
    out.release()

def generate_gif(
    input_video_path:str,
    output_gif_path:str,
    scale:int=600,
    fps:int=10,
    colors:int=128
):
    """
    Generate GIF file for usage in the steam page 
    show preview of gameplay in description
    :param input_video_path: video path to be converted
    :param output_gif_path: output path to be generate
    :param scale: scale of the gif file
    :param fps: fps amount of the gif file
    :param colors: color number of the gif file
    """
    input_video_path = os.path.abspath(input_video_path)
    output_gif_path = os.path.abspath(output_gif_path)
    
    errors = []
    palette_path = "palette.png"
    command_palette = [
        "ffmpeg", "-i", input_video_path, 
        "-vf", f"fps={fps},scale={scale}:-1:flags=lanczos,palettegen=max_colors={colors}", 
        "-y", palette_path
    ]
    result  = subprocess.run(command_palette, capture_output=True, text=True)
    if result.returncode != 0:
        errors.append(result.stderr)
    
    command_gif = [
        "ffmpeg", "-i", input_video_path, "-i", palette_path, 
        "-filter_complex", f"fps={fps},scale={scale}:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=sierra2",
        "-y", output_gif_path
    ]

    result = subprocess.run(command_gif, capture_output=True, text=True)
    if result.returncode != 0:
        errors.append(result.stderr)
    
    if len(errors):
        print(mdxutils.Colors.colprint('GIF generator error: ', mdxutils.Colors.FAIL), errors)
    else:
        print(mdxutils.Colors.colprint('GIF successful generated', mdxutils.Colors.OKGREEN))

def processor(
    abspath:str,
    base_path:str,
    filename:str,
    output_path:str=None,
    action:str="0",
    scale:int=600,
    fps:int=10,
    colors:int=128,
    index:int=0
):
    if action == "0": # create gif
        output_path = output_path if output_path.strip() else base_path
        output_gif_path = mdxutils.generate_output_name(output_path, filename, extension='gif')
        generate_gif(abspath, output_gif_path, scale, fps, colors)
    elif action == '1': # upscaling
        ext = filename.split('.')[1]
        
        temp_audio_path = './copycat/temp_audio.mp3'
        temp_video_path = f'./copycat/temp_video.{ext}' # r'out_frames\frames_%04d.jpg'
        upscaled_video_path = mdxutils.generate_output_name(base_path, filename, index=index)
        
        extract_audio(abspath, temp_audio_path) # Step 1: Extract audio
        upscale_video(abspath, temp_video_path, ext, index) # Step 2: Upscale video
        combine_video_audio(temp_video_path, temp_audio_path, upscaled_video_path) # Step 3: Combine upscaled video with audio

        os.remove(temp_audio_path)
        os.remove(temp_video_path)

action = str(input("Action (0 - Create GIF 1 - Upscaling): "))
base_path = str(input("Basedir: "))
extra_params = {"action": action}
if action == "0":
    output_path = str(input("Outputdir(Basedir): "))
    _scale = str(input("Scale(600): "))
    _fps = str(input("FPS(10): "))
    _colors = str(input("Colors(128): "))

    _scale = int(_scale) if _scale.strip() else 600
    _fps = int(_fps) if _fps.strip() else 10
    _colors = int(_colors) if _colors.strip() else 128

    extra_params = {
        **extra_params,
        "output_path":output_path,
        "scale":_scale,
        "fps":_fps,
        "colors":_colors,
    }
elif action == '1': 
    _index = str(input(f"Resolution ({mdxutils.resolution_available()}): "))
    _index = int(_index) if mdxutils.is_valid_number(_index) and mdxutils.resolution_valid(int(_index)) else 0
    extra_params = {
        **extra_params,
        "index": _index
    }
else:
    print(mdxutils.Colors.colprint('Invalid action...', mdxutils.Colors.FAIL))
    exit()

mdxutils.get_dir_files(base_path, processor, **extra_params)
