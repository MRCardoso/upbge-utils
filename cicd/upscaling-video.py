import cv2
import ffmpeg
import sys
import os

def print_progress_bar(percentage):
    bar_length = 50
    filled_length = int(bar_length * percentage / 100)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\r[{bar}] {percentage:.2f}%')
    sys.stdout.flush()

def upscale_video(input_path, output_path):
    # Open the input video
    cap = cv2.VideoCapture(input_path)

    
    # normalize video path
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)
    
    # get the original video's width and height
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    
     # Get the original video's properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    # define the desired width and height (4k resolution)
    width = 3840
    height = 2160

    #define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('temp.mp4', fourcc, fps, (width, height))
    
    frame_number = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # resize frame
        resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)
        
        #write the resized frame
        out.write(resized_frame)

         # Update the progress bar
        frame_number += 1
        percentage = (frame_number / frame_count) * 100
        print_progress_bar(percentage)

    # relese everything
    cap.release()
    out.release()

    # use ffmpeg to convert the output to desired format and optimize
    ffmpeg.input('temp.mp4').output(output_path).run()

# usage
if len(sys.argv) < 3:
    print("please provide input and output path")
    exit()

base_path = sys.argv[1]
filename = str(sys.argv[2])
filename, ext = filename.split('.')

upscale_video(f'{base_path}/{filename}.{ext}', f'{base_path}/{filename}-4k.{ext}')
