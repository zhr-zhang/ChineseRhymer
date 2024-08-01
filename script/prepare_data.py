import re
from typing import List, Dict
from tqdm import tqdm
import json
import os

standard_character_paths = [
    "resource/standard_table/level-1.txt",
    "resource/standard_table/level-2.txt",
    "resource/standard_table/level-3.txt",
]
simple_formatted_files = [
    "resource/words_data/中文分词词库整理/dict.txt",
    "resource/words_data/中文分词词库整理/fingerDic.txt",
    "resource/words_data/中文分词词库整理/httpcws_dict.txt",
    "resource/words_data/中文分词词库整理/out.txt",
    "resource/words_data/中文分词词库整理/五笔词库.TXT",
    "resource/words_data/中文分词词库整理/四十万汉语大词库.txt",
    "resource/words_data/停用词/中文停用词库.txt",
    "resource/words_data/停用词/哈工大停用词表.txt",
    "resource/words_data/停用词/四川大学停用词表.txt",
    "resource/words_data/停用词/百度停用词表.txt",
    "resource/words_data/成语词库/ChengYu_Corpus（5W）.txt",
    "resource/words_data/中文分词词库整理/30wdict.txt",
]
THUOCL_formatted_files = [
    "resource/words_data/动物词库/THUOCL_animal.txt",
    "resource/words_data/医学词库/THUOCL_medical.txt",
    "resource/words_data/成语词库/THUOCL_chengyu.txt",
    "resource/words_data/法律词库/THUOCL_law.txt",
    "resource/words_data/财经词库/THUOCL_caijing.txt",
    "resource/words_data/食物词库/THUOCL_food.txt",
    "resource/words_data/中文分词词库整理/四十万可用搜狗txt词库.txt",
]
dest_dependencies_dir = "dependencies"
dest_characters_path = "dependencies/characters.txt"
dest_character_pinyin_dict_path = "dependencies/character_pinyin_dict.json"
dest_words_path = "dependencies/words.txt"

characters_texts: List[str] = []
print("Preparing characters...")
for standard_character_path in standard_character_paths:
    with open(standard_character_path, "r", encoding="utf-8") as f:
        characters_texts.extend(f.readlines())
standard_characters = [info.strip().split(",")[2] for info in characters_texts]

with open("resource/pinyins_resource.txt", "r", encoding="utf-8") as f:
    print("Preparing pinyins...")
    pinyins_texts = f.readlines()
    characters_with_pinyin: List[str] = []
    character_pinyin_dict: Dict[str, str] = {}
    for text in pinyins_texts:
        parts = text.strip().split(" ")
        if len(parts) != 6:
            continue
        character = parts[4]
        pinyin = parts[2].replace(";", "").replace('"', "")
        if character not in standard_characters:
            continue
        if character in characters_with_pinyin:
            pinyin = character_pinyin_dict[character] + "," + pinyin
        else:
            characters_with_pinyin.append(character)
        character_pinyin_dict[character] = pinyin
    standard_characters = characters_with_pinyin


def filter_words_with_standard_characters(words: List[str]) -> List[str]:
    filtered_words: List[str] = []
    for word in tqdm(words, desc="Filtering words with standard characters"):
        if all([character in standard_characters for character in word]):
            filtered_words.append(word)
    return filtered_words


def strip_words(words: List[str]) -> List[str]:
    print("Stripping words...")
    return [word.strip() for word in words]


def filter_repeated_words(words: List[str]) -> List[str]:
    print("Filtering repeated words...")
    return list(set(words))


def prepare_words() -> List[str]:
    print("Preparing words...")
    words: List[str] = []
    for file in simple_formatted_files:
        with open(file=file, mode="r", encoding="utf-8") as f:
            words.extend(f.readlines())
    for file in THUOCL_formatted_files:
        with open(file=file, mode="r", encoding="utf-8") as f:
            words.extend([line.split(" ")[0] for line in f.readlines()])

    with open(
        file="resource/words_data/中文分词词库整理/42537条伪原创词库.txt",
        mode="r",
        encoding="utf-8",
    ) as f:
        words_text: List[str] = []
        for line in f.readlines():
            words_in_line = line.split("→")
            for word_in_line in words_in_line:
                words_text.append(word_in_line)
        words.extend(words_text)
    with open(file="resource/XDHYCD7th.txt", mode="r", encoding="utf-8") as f:
        xhzd = f.read()
        pattern = re.compile(r"【(.*?)】")
        matches: List[str] = pattern.findall(xhzd)
        cleaned_matches = {re.sub(r"（儿）", "", match) for match in matches}
        words.extend(cleaned_matches)

    words = strip_words(words)
    words = filter_repeated_words(words)
    words = filter_words_with_standard_characters(words)
    return words


os.makedirs(dest_dependencies_dir, exist_ok=True)
with open(dest_characters_path, "w", encoding="utf-8") as f:
    for character in standard_characters:
        f.write(character + "\n")
with open(dest_character_pinyin_dict_path, "w", encoding="utf-8") as file:
    json.dump(character_pinyin_dict, file, ensure_ascii=False, indent=4)
with open(dest_words_path, "w", encoding="utf-8") as f:
    words = prepare_words()
    for word in words:
        f.write(word + "\n")
