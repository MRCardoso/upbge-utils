from io import TextIOWrapper
import autoloader
from googletrans import Translator
import mdxutils

import json
import sys
import vdf
import os

from CrossLanguage import texts, titles

mode = input("Mode (1 - texts, 2 - titles, 3 - file): ")
mode = int(mode) if mdxutils.is_valid_number(mode) else 1
target_language = str(input("Lang (pt, es, ja): "))
target_language = target_language.strip() if target_language.strip() else "pt"

def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

def _process_vdf_file(file, target_language):
    languages = {
        "en": "engish",
        "pt": "brazilian",
    }
    decoded = vdf.parse(file)
    output = {}
    items = decoded['lang']['Tokens']
    total_items = len(items)
    index = 0
    for lk in items:
        mdxutils.print_progress_bar(
            ((index + 1) / total_items) * 100
        )
        output[lk] = translate_text(items[lk], target_language)
        index += 1

    return vdf.dumps({"lang": {languages[target_language]: { "Tokens": output }}}, pretty=True)

def _process_text_file(file: TextIOWrapper):
    _lines = file.readlines()
    size = len(_lines)
    output = []
    for i, value in enumerate(_lines):
        mdxutils.print_progress_bar(
            ((i + 1) / size) * 100
        )
        output.append(translate_text(value, target_language))
    
    return "\n".join(output)

def _process_dzaj_content(source_content):
    output = {}
    total_items = len(source_content)
    for index, i in enumerate(source_content):
        textSize = len(source_content[i])
        percentage = ((index + 1) / total_items) * 100
        mdxutils.print_progress_bar(percentage)
        if len(source_content[i][0]) > 0 and (textSize == 1 or textSize == 2 and not str(source_content[i][1]).strip()):
            text_to_translate = source_content[i][0]
            if isinstance(text_to_translate, list):
                text_to_translate = '\n'.join(text_to_translate)
            translated_text = translate_text(text_to_translate, target_language)
            output[i] = [
                text_to_translate,
                translated_text
            ]
    
    return output

data = {}
if mode == 3:
    file_path = input("Filename: ")
    source_file = os.path.basename(file_path)
    ext = source_file.split('.')
    if len(ext) == 2:
        ext = ext[1]
        with open(os.path.abspath(file_path), 'r', encoding='utf-8') as file:
            if ext == 'vdf':
                data = _process_vdf_file(file, target_language)
            elif ext == 'txt':
                data = _process_text_file(file)
    else:
        data = translate_text(source_file, target_language)
        source_file = 'inline.txt'
else:
    if mode == 2:
        source_content = titles
        source_file = 'titles.py'
    else:
        source_content = texts
        source_file = 'texts.py'
    data = _process_dzaj_content(source_content)

if len(data):
    with open(f"copycat/{source_file}", "w", encoding="utf-8") as file_content:
        ext_ = source_file.split('.')[1]
        if ext_ == "py":
            json.dump(data, file_content, indent=4, ensure_ascii=False)
        else:
            file_content.write(data)
