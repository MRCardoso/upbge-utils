import sys
import os

file_name = os.path.join(os.getcwd(), 'add_extra_path.txt')

if os.path.isfile(file_name):
    with open(file_name, 'r') as f:
        relative_path_to_extra_path	= f.read()
    sys.path.append(relative_path_to_extra_path)

os.environ['LD_LIBRARY_PATH'] = os.getcwd()