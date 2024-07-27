import json
from tqdm import tqdm

characters = open("resource/characters.txt", "r", encoding="utf-8").readlines()
pinyins_path = "resource/kXHC1983.txt"

# 创建character_pinyin_dict
character_pinyin_dict = {}
with open(pinyins_path, "r", encoding="utf-8") as file:
    for line in tqdm(file):
        for character in characters:
            character = character.strip()
            if character in line:
                pinyin = line.split(" ")[1]
                character_pinyin_dict[character] = pinyin
# 写json
with open("resource/character_pinyin_dict.json", "w", encoding="utf-8") as file:
    json.dump(character_pinyin_dict, file, ensure_ascii=False, indent=4)
