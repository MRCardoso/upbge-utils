import os
import vdf

file_path = 'F:\\MardozuxStudio\\Game-007\\701905\\achievements\\3005310_loc_all.vdf'
with open(os.path.abspath(file_path), 'r', encoding='utf-8') as file:
    decoded = vdf.parse(file)
    for lang in decoded["lang"]:
        for texts in decoded["lang"][lang]["Tokens"]:
            # print(f'{decoded["lang"][lang]["Tokens"][texts]}', end='', flush=True)
            message = f'Progress: {texts}/10'
            print(f'\r{message}', end='', flush=True)
            input('')