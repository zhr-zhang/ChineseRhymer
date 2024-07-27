from typing import List
import re
import json
from tqdm import tqdm

# Define file paths
standard_character_paths = [
    "reference/standard_table/level-1.txt",
    "reference/standard_table/level-2.txt",
    "reference/standard_table/level-3.txt",
]
character_path = "resource/characters.txt"
kxdzd_path = "resource/kXHC1983.txt"
xdhycd_path = "resource/XDHYCD7th.txt"
word_path = "resource/words.txt"
character_pinyin_dict_path = "resource/character_pinyin_dict.json"

# Read standard character files and extract characters
characters_texts: List[str] = []
for standard_character_path in standard_character_paths:
    with open(standard_character_path, "r", encoding="utf-8") as f:
        characters_texts += f.readlines()
characters = [info.strip().split(",")[2] for info in characters_texts]

# Read kxdzd file and extract characters with pinyin
with open(kxdzd_path, "r", encoding="utf-8") as f:
    infos2 = f.readlines()
characters_with_pinyin = [info.split(" ")[2].strip() for info in infos2]
characters = [
    character for character in characters if character in characters_with_pinyin
]

# Write filtered characters to character_path
with open(character_path, "w", encoding="utf-8") as f:
    for character in characters:
        f.write(character + "\n")

# Extract and clean words from xdhycd_path
xhzd = open(xdhycd_path, "r", encoding="utf-8").read()
pattern = re.compile(r"【(.*?)】")
matches: List[str] = pattern.findall(xhzd)
cleaned_matches = {re.sub(r"（儿）", "", match) for match in matches}

# Filter valid words
words_text = set(cleaned_matches)
valid_words_text = {
    word
    for word in words_text
    if all(char in characters for char in word) and len(word) >= 2
}

# Write valid words to word_path
with open(word_path, "w", encoding="utf-8") as f:
    for word in valid_words_text:
        f.write(word + "\n")

# Create character to pinyin dictionary
character_pinyin_dict = {}
with open(kxdzd_path, "r", encoding="utf-8") as file:
    for line in file:
        parts = line.split(" ")
        character = parts[2].strip()
        if character in characters:
            pinyin = parts[1].strip()
            character_pinyin_dict[character] = pinyin

# Write character to pinyin dictionary to character_pinyin_dict_path
with open(character_pinyin_dict_path, "w", encoding="utf-8") as file:
    json.dump(character_pinyin_dict, file, ensure_ascii=False, indent=4)
