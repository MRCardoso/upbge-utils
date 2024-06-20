import json
import sys
from googletrans import Translator

def translate_text(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='pt')
    return translated_text.text

def print_progress_bar(percentage):
    bar_length = 50
    filled_length = int(bar_length * percentage / 100)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\r[{bar}] {percentage:.2f}%')
    sys.stdout.flush()

def normalizeTextUI(original, width=60, height=6):
    _words = str(original).split()
    _normalized = []
    _current_line = []

    for word in _words:
        if len(' '.join(_current_line)) + len(word) <= width:
            _current_line.append(word)
        else:
            _normalized.append(' '.join(_current_line))
            _current_line = [word]

    if _current_line:
        _normalized.append(' '.join(_current_line))

    _rows = []
    _normalizedGroup = []
    for v in _normalized:
        if len(_rows) <= height:
            _rows.append(v)
        else:
            _normalizedGroup.append(' '.join(_rows))
            _rows = [v]
    
    if len(_rows):
        _normalizedGroup.append(' '.join(_rows))

    return _normalizedGroup

with open(f"cicd/copycat/raw.txt", "r", encoding="utf-8") as file:
    _lines = file.readlines()
    # _lines = normalizeTextUI(_raw)
    size = len(_lines)
    data = {}
    dataLines = "" 
    _i = 1
    index="03"
    # _lines = filter(lambda x: str(x).strip(), _lines)
    
    for i, value in enumerate(_lines):
        percentage = ((i + 1) / size) * 100
        print_progress_bar(percentage)
        if value.strip():
            _itext = str(_i).rjust(2, '0')
            data[f'file{index}_{_itext}'] = [
                value.replace("\n", ""),
                translate_text(value)
            ]
            _i += 1
            dataLines = ""
        else:
            dataLines += "\n\n"

    with open(f"cicd/copycat/listed.py", "w", encoding="utf-8") as file_content:
        json.dump(data, file_content, indent=4, ensure_ascii=False)