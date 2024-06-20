import subprocess
import os
import sys
import re

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
        print('GIF generator error: ', errors)
    else:
        print('GIF successful generated')

base_path = str(input("Basedir: "))
output_path = str(input("Outputdir(Basedir/gifs): "))
files_and_directories = os.listdir(base_path)

for item in files_and_directories:
    if os.path.isfile(os.path.join(base_path, item)):
        _process = str(input(f"{item} convert[y/n]? "))
        if str(_process).lower() == 'x':
            break
        elif str(_process).lower() != 'y':
            continue
        _scale = str(input("Scale(600): "))
        _fps = str(input("FPS(10): "))
        _colors = str(input("Colors(128): "))

        output_path = output_path if output_path.strip() else f"{base_path}/gifs"
        _scale = int(_scale) if _scale.strip() else 600
        _fps = int(_fps) if _fps.strip() else 10
        _colors = int(_colors) if _colors.strip() else 128

        input_video_path = f'{base_path}/{item}'
        output_gif_path = f'{output_path}/{item.split('.')[0]}.gif'

        generate_gif(input_video_path, output_gif_path, _scale, _fps, _colors)
