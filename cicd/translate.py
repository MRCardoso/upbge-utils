import autoloader
from googletrans import Translator
import mdxutils

import json
import sys

from CrossLanguage import texts, titles

mode = input("Mode (1 - texts, 2 - titles): ")
mode = int(mode) if mdxutils.is_valid_number(mode) else 1
target_language = str(input("Lang (pt, es, ja): "))
target_language = target_language.strip() if target_language.strip() else "pt"

def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text

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
    mdxutils.print_progress_bar(percentage)
    if len(source_content[i][0]) > 0 and (textSize == 1 or textSize == 2 and not str(source_content[i][1]).strip()):
        text_to_translate = source_content[i][0]
        if isinstance(text_to_translate, list):
            text_to_translate = '\n'.join(text_to_translate)
        translated_text = translate_text(text_to_translate, target_language)
        data[i] = [
            text_to_translate,
            translated_text
        ]

if len(data):
    with open(f"copycat/{source_file}.py", "w", encoding="utf-8") as file_content:
        json.dump(data, file_content, indent=4, ensure_ascii=False)
