import os
import re
import sys

RESOLUTIONS = [
    (3840, 2160),  # 4K
    (2560, 1440),  # 2K
    (1920, 1080),  # Full HD
]
RESOLUTION_LABEL = (
    '4K',
    '2K',
    'full-HD',
)

PIXEL_SIZES = [
    # (16, 16),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256)
]


def is_valid_number(value) -> bool:
    return re.search(r'^\d$', value)

def resolution_valid(index:int) -> bool:
    return index >= 0 and index <= (len(RESOLUTIONS)-1)

def pixel_valid(index:int) -> bool:
    return index >= 0 and index <= (len(PIXEL_SIZES)-1)

def resolution_available() -> list[str]:
    return [f"{i} - {x[0]}x{x[1]}" for i, x in enumerate(RESOLUTIONS)]

def pixel_available() -> list[str]:
    return [f"{i} - {x[0]}x{x[1]}" for i, x in enumerate(PIXEL_SIZES)]

def generate_output_name(base_path:str, filename:str, index:int=None, extra:str='', extension=None) -> str:
    ext = extension if extension else filename.split('.')[1]
    extra = f'-{extra}' if str(extra).strip() else ''
    index = f'-{RESOLUTION_LABEL[index]}' if index != None else ''
    return os.path.abspath(f'{base_path}/{filename.split('.')[0]}-out{extra}{index}.{ext}')


def print_progress_bar(percentage):
    bar_length = 50
    filled_length = int(bar_length * percentage / 100)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\r[{bar}] {percentage:.2f}%')
    sys.stdout.flush()

def get_dir_files(base_path: str, callback, **kwargs) -> None:
    files_and_directories = os.listdir(base_path)

    for item in files_and_directories:
        if not os.path.isfile(os.path.join(base_path, item)):
            continue
        _process = str(input(f"{item} run[y/n]? "))
        if str(_process).lower() == 'x':
            break
        elif str(_process).lower() != 'y':
            continue
        callback(abspath=os.path.abspath(f"{base_path}/{item}"), base_path=base_path, filename=item, **kwargs)


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'  # Reset to default color
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def colprint(text, color):
        return f"{color}{text}{Colors.ENDC}"