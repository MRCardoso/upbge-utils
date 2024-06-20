import sys
import os

file_name = os.path.join(os.getcwd(), 'cicd', 'add_extra_path.txt')
if os.path.isfile(file_name):
    print(file_name)
    with open(file_name, 'r') as f:
        relative_path_to_extra_path	= f.read()
        print(relative_path_to_extra_path)
    sys.path.append(relative_path_to_extra_path)

os.environ['LD_LIBRARY_PATH'] = os.getcwd()