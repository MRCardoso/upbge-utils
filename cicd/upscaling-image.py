from PIL import Image, ImageFilter
import sys
import os
import cv2
import numpy as np

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

def apply_pillow(input_path, output_path, resolution_index=0, apply_sharpening=False):
    # open the input image
    image = Image.open(input_path)
    # Resize the image using high-quality resampling (Lanczos filter)
    upscaled_image = image.resize(resolutions[resolution_index], Image.LANCZOS)
    if apply_sharpening:
        # Apply a sharpening filter
        upscaled_image = upscaled_image.filter(ImageFilter.SHARPEN)
    # Save the upscaled and enhanced image
    upscaled_image.save(output_path)

def apply_opencv(input_path, output_path, resolution_index=0, apply_sharpening=False):
    # Read the input image
    image = cv2.imread(input_path)
    
    # Resize the image using cubic interpolation
    upscaled_image = cv2.resize(image, resolutions[resolution_index], interpolation=cv2.INTER_CUBIC)
    
    if apply_sharpening:
        # Apply sharpening kernel
        kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
        upscaled_image = cv2.filter2D(upscaled_image, -1, kernel)
    
    # Save the upscaled and enhanced image
    cv2.imwrite(output_path, upscaled_image)

    

def upscaling(input_path, output_path, mode='opencv', index=0, sharp=False):
    # normalize images path
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)

    if mode == 'opencv':
        apply_opencv(input_path, output_path, index, apply_sharpening=sharp)
    elif mode == 'pillow':
        apply_pillow(input_path, output_path, index, apply_sharpening=sharp)
    
    

if len(sys.argv) < 3:
    print("please provide input and output path")
    exit()

base_path = sys.argv[1]
filename = str(sys.argv[2])
filename, ext = filename.split('.')
_mode = 'pillow'
_sharp = True
_index = 0

if len(sys.argv) > 3:
    _mode = 'opencv' if int(sys.argv[3]) == 1 else 'pillow'

if len(sys.argv) > 4:
    if int(sys.argv[4]) >= 0 and int(sys.argv[4]) <= (len(resolutions)-1):
        _index = int(sys.argv[4])

if len(sys.argv) > 5:
    _sharp = True if int(sys.argv[5]) == 1 else False

upscaling(
    f'{base_path}/{filename}.{ext}',
    f'{base_path}/{filename}-{extra_resolution[_index]}.{ext}',
    _mode,
    _index,
    _sharp
)