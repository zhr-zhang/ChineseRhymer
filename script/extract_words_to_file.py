import re
from word import Word
from character import Character
from typing import List
from tqdm import tqdm

# 文件路径
word_path = "resource/XDHYCD7th.txt"
character_path = "resource/characters.txt"
output_path = "resource/words.txt"

# 读取字符文件
with open(character_path, "r") as f:
    infos = f.readlines()
characters = [Character(info) for info in infos]

# 读取词文件
text = open(word_path, "r", encoding="utf-8").read()
pattern = re.compile(r"【(.*?)】")
matches: List[str] = pattern.findall(text)
words_text = set(matches)

character_set = set([char.character for char in characters])

valid_words_text = set()
for word in tqdm(words_text, desc="Progress"):
    if all(character in character_set for character in word):
        if len(word) >= 2:
            valid_words_text.add(word)

with open(output_path, "w", encoding="utf-8") as f:
    for word in valid_words_text:
        f.write(word + "\n")

# words = [Word(word) for word in valid_words_text]