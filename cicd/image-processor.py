import shutil
from PIL import Image, ImageFilter
import sys
import os
import cv2
import re
import numpy as np
import subprocess
import mdxutils
"""
Thrid Part Libs
- ffmpeg
- cv2
- numpy
- PIL
- https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan
"""

def apply_pillow(input_path, output_path, resolution_index=0, apply_sharpening=False):
    image = Image.open(input_path)
    upscaled_image = image.resize(mdxutils.RESOLUTIONS[resolution_index], Image.LANCZOS)
    if apply_sharpening:
        upscaled_image = upscaled_image.filter(ImageFilter.SHARPEN)
    upscaled_image.save(output_path)

def apply_superres(input_image_path, output_image_path, mode=0):
    command_superres = [
        "./realesrgan-windows/realesrgan-ncnn-vulkan.exe",
        "-i", input_image_path,
        "-o", output_image_path, 
        # "-n", "realesrgan-x4plus"
    ]
    result  = subprocess.run(command_superres, capture_output=True, text=True)
    if result.returncode != 0:
        print(mdxutils.Colors.colprint("Processor Error", mdxutils.Colors.FAIL), result.stderr)


def upscaling(
    abspath:str, base_path:str, filename:str, mode:str='superres', index:int=0, sharp:bool=False
        # input_path, output_path, mode='opencv', index=0, sharp=False
):
    output_path = mdxutils.generate_output_name(base_path, filename, index, mode)

    if mode == 'pillow':
        apply_pillow(abspath, output_path, index, apply_sharpening=sharp)
    elif mode == 'superres':
        apply_superres(abspath, output_path, index)
    
    print(mdxutils.Colors.colprint('Upscaling successful', mdxutils.Colors.OKGREEN))

base_path = str(input("Basedir: "))
_mode = str(input("Mode (0 - Super Resolution, 1 - pillow): "))
_index = str(input(f"Resolution ({mdxutils.resolution_available()}): "))
_mode = 'pillow' if mdxutils.is_valid_number(_mode) and int(_mode) == 1 else 'superres'
_index = int(_index) if mdxutils.is_valid_number(_index) and mdxutils.resolution_valid(int(_index)) else 0
_sharp = False

if _mode == 'pillow':
    _sharp = str(input("Sharpening (1 - True, 0 - False): "))
    _sharp = False if mdxutils.is_valid_number(_sharp) and int(_sharp) == 0 else True

mdxutils.get_dir_files(base_path, upscaling, mode=_mode, index=int(_index), sharp=_sharp)

# upscaling(
#     f'{base_path}/{filename}.{ext}',
#     f'{base_path}/{filename}-{_mode}-{extra_resolution[_index]}.{ext}',
#     _mode,
#     _index,
#     _sharp
# )