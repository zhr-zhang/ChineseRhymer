import re
from word import Word
from character import Character
from typing import List
from tqdm import tqdm

character_path = "resource/level-1.txt"
output_path = "resource/characters.txt"
pinyin_path = "data/kXHC1983.txt"

# 读取字符文件
with open(character_path, "r") as f:
    infos1 = f.readlines()
characters1 = [info.split(",")[2] for info in infos1]
with open(pinyin_path, "r") as f:
    infos2 = f.readlines()
characters2 = [info.split(" ")[2].replace("\n", "") for info in infos2]

with open(output_path, "w", encoding="utf-8") as f:
    for character in characters1:
        if character in characters2:
            f.write(character + "\n")
