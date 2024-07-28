from typing import List
import re
import json
import os

# 定义文件路径
standard_character_paths = [
    "resource/standard_table/level-1.txt",
    "resource/standard_table/level-2.txt",
    "resource/standard_table/level-3.txt",
]
characters_path = "dependencies/characters.txt"
character_pinyin_dict_path = "dependencies/character_pinyin_dict.json"
words_path = "dependencies/words.txt"
XDHYCD7th_path = "resource/XDHYCD7th.txt"
pinyins_path = "resource/pinyins_resource.txt"
dependenciesz_dir = "dependencies/"

# 读取标准字符文件
characters_texts: List[str] = []
for standard_character_path in standard_character_paths:
    with open(standard_character_path, "r", encoding="utf-8") as f:
        characters_texts += f.readlines()

standard_characters = [info.strip().split(",")[2] for info in characters_texts]

# 读取拼音数据
with open(pinyins_path, "r", encoding="utf-8") as f:
    pinyins_texts = f.readlines()

# 过滤有拼音的字符
characters_with_pinyin = []
character_pinyin_dict = {}
for text in pinyins_texts:
    parts = text.strip().split(" ")
    if len(parts) != 6:
        continue
    character = parts[4]
    if character not in standard_characters:
        continue
    pinyin = parts[2].replace(";", "").replace('"', "")
    character_pinyin_dict[character] = pinyin
    characters_with_pinyin.append(character)

characters = [
    character
    for character in standard_characters
    if character in characters_with_pinyin
]

# 从字典中提取和清理词语
with open(XDHYCD7th_path, "r", encoding="utf-8") as f:
    xhzd = f.read()
pattern = re.compile(r"【(.*?)】")
matches: List[str] = pattern.findall(xhzd)
cleaned_matches = {re.sub(r"（儿）", "", match) for match in matches}

# 过滤有效词语
words_text = set(cleaned_matches)
valid_words_text = {
    word
    for word in words_text
    if all(char in characters for char in word) and len(word) >= 2
}

os.makedirs(dependenciesz_dir, exist_ok=True)

# 将字符和词语写入文件
with open(characters_path, "w", encoding="utf-8") as f:
    for character in characters:
        f.write(character + "\n")

with open(words_path, "w", encoding="utf-8") as f:
    for word in valid_words_text:
        f.write(word + "\n")

# 将字符到拼音的字典写入文件
with open(character_pinyin_dict_path, "w", encoding="utf-8") as file:
    json.dump(character_pinyin_dict, file, ensure_ascii=False, indent=0)
