import autoloader

from googletrans import Translator
from tabulate import tabulate

import json
import sys

from CrossLanguage import texts, titles

mode = 1
if len(sys.argv) > 1:
    mode = int(sys.argv[1])
if mode not in [1, 2]:
    print("Invalid translate (1 - texts, 2 - titles)")
    exit()

def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

def print_progress_bar(percentage):
    bar_length = 50
    filled_length = int(bar_length * percentage / 100)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\r[{bar}] {percentage:.2f}%')
    sys.stdout.flush()

data = {}
source_content = None
if mode == 2:
    source_content = titles
    source_file = 'titles'
else:
    source_content = texts
    source_file = 'texts'

total_items = len(source_content)
for index, i in enumerate(source_content):
    textSize = len(source_content[i])
    percentage = ((index + 1) / total_items) * 100
    print_progress_bar(percentage)
    if len(source_content[i][0]) > 0 and (textSize == 1 or textSize == 2 and not str(source_content[i][1]).strip()):
        text_to_translate = source_content[i][0] #input("Text: ")
        target_language = "pt" # input("Lang: ")
        translated_text = translate_text(text_to_translate, target_language)
        data[i] = [
            text_to_translate,
            translated_text
        ]

if len(data):
    with open(f"cicd/copycat/{source_file}.py", "w", encoding="utf-8") as file_content:
        json.dump(data, file_content, indent=4, ensure_ascii=False)
