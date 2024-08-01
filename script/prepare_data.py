import re
from typing import List, Set
from tqdm import tqdm
import json
import os


standard_character_paths = [
    "resource/standard_table/level-1.txt",
    "resource/standard_table/level-2.txt",
    "resource/standard_table/level-3.txt",
]
characters_path = "dependencies/characters.txt"
character_pinyin_dict_path = "dependencies/character_pinyin_dict.json"
words_path = "dependencies/words.txt"
pinyins_path = "resource/pinyins_resource.txt"
dependenciesz_dir = "dependencies/"
characters_texts: List[str] = []
for standard_character_path in standard_character_paths:
    with open(standard_character_path, "r", encoding="utf-8") as f:
        characters_texts += f.readlines()
standard_characters = [info.strip().split(",")[2] for info in characters_texts]
# 读取拼音数据
with open("resource/pinyins_resource.txt", "r", encoding="utf-8") as f:
    pinyins_texts = f.readlines()
    characters_with_pinyin = []
    character_pinyin_dict = {}
    for text in pinyins_texts:
        parts = text.strip().split(" ")
        if len(parts) != 6:
            continue
        character = parts[4]
        pinyin = parts[2].replace(";", "").replace('"', "")
        if character in characters_with_pinyin:
            pinyin = character_pinyin_dict[character] + "," + pinyin
        else:
            characters_with_pinyin.append(character)
        character_pinyin_dict[character] = pinyin

standard_characters = [
    character
    for character in standard_characters
    if character in characters_with_pinyin
]


def filter_words_with_standard_characters(words: List[str]) -> List[str]:
    filtered_words: List[str] = []
    for word in tqdm(words, desc="Filtering words with standard characters:"):
        word = word.strip()
        if all([character in standard_characters for character in word]):
            filtered_words.append(word)
    return filtered_words


def filter_repeated_words(words: List[str]) -> List[str]:
    return list(set(words))


def prepare_words() -> List[str]:

    words: List[str] = []
    with open("resource/words_data/中文分词词库整理/30wdict.txt", "r") as f:
        words_text: List[str] = f.readlines()
        words.extend(words_text)
    with open("resource/words_data/中文分词词库整理/42537条伪原创词库.txt", "r") as f:
        words_text = []
        lines = f.readlines()
        for line in lines:
            words_in_line = line.split("→")
            for word_in_line in words_in_line:
                words_text.append(word_in_line)
        words.extend(words_text)
    with open("resource/words_data/中文分词词库整理/dict.txt", "r") as f:
        words_text = f.readlines()
        words.extend(words_text)
    with open("resource/words_data/中文分词词库整理/fingerDic.txt", "r") as f:
        words_text = f.readlines()
        words.extend(words_text)
    with open("resource/words_data/中文分词词库整理/httpcws_dict.txt", "r") as f:
        words_text = f.readlines()
        words.extend(words_text)
    with open("resource/words_data/中文分词词库整理/out.txt", "r") as f:
        words_text = f.readlines()
        words.extend(words_text)
    with open("resource/words_data/中文分词词库整理/五笔词库.TXT", "r") as f:
        words_text = f.readlines()
        words.extend(words_text)
    with open(
        "resource/words_data/中文分词词库整理/四十万可用搜狗txt词库.txt", "r"
    ) as f:
        words_text = f.readlines()
        words_text = [line.split(" ")[0] for line in words_text]
        words.extend(words_text)
    with open("resource/words_data/中文分词词库整理/四十万汉语大词库.txt", "r") as f:
        words_text = f.readlines()
        words.extend(words_text)
    with open("resource/words_data/停用词/中文停用词库.txt", "r") as f:
        words_text = f.readlines()
        words.extend(words_text)
    with open("resource/words_data/停用词/哈工大停用词表.txt", "r") as f:
        words_text = f.readlines()
        words.extend(words_text)
    with open("resource/words_data/停用词/四川大学停用词表.txt", "r") as f:
        words_text = f.readlines()
        words.extend(words_text)
    with open("resource/words_data/停用词/百度停用词表.txt", "r") as f:
        words_text = f.readlines()
        words.extend(words_text)
    with open("resource/words_data/成语词库/ChengYu_Corpus（5W）.txt", "r") as f:
        words_text = f.readlines()
        words.extend(words_text)
    with open("resource/words_data/动物词库/THUOCL_animal.txt", "r") as f:
        words_text = [line.split(" ")[0] for line in f.readlines()]
        words.extend(words_text)
    with open("resource/words_data/医学词库/THUOCL_medical.txt", "r") as f:
        words_text = [line.split(" ")[0] for line in f.readlines()]
        words.extend(words_text)
    with open("resource/words_data/成语词库/THUOCL_chengyu.txt", "r") as f:
        words_text = [line.split(" ")[0] for line in f.readlines()]
        words.extend(words_text)
    with open("resource/words_data/法律词库/THUOCL_law.txt", "r") as f:
        words_text = [line.split(" ")[0] for line in f.readlines()]
        words.extend(words_text)
    with open("resource/words_data/财经词库/THUOCL_caijing.txt", "r") as f:
        words_text = [line.split(" ")[0] for line in f.readlines()]
        words.extend(words_text)
    with open("resource/words_data/食物词库/THUOCL_food.txt", "r") as f:
        words_text = [line.split(" ")[0] for line in f.readlines()]
        words.extend(words_text)
    with open("resource/XDHYCD7th.txt", "r", encoding="utf-8") as f:
        xhzd = f.read()
        pattern = re.compile(r"【(.*?)】")
        matches: List[str] = pattern.findall(xhzd)
        cleaned_matches = {re.sub(r"（儿）", "", match) for match in matches}
        words.extend(cleaned_matches)
    words = filter_repeated_words(words)
    words = filter_words_with_standard_characters(words)
    return words


os.makedirs(dependenciesz_dir, exist_ok=True)
with open(characters_path, "w", encoding="utf-8") as f:
    for character in standard_characters:
        f.write(character + "\n")
with open(character_pinyin_dict_path, "w", encoding="utf-8") as file:
    json.dump(character_pinyin_dict, file, ensure_ascii=False, indent=4)
with open(words_path, "w", encoding="utf-8") as f:
    words = prepare_words()
    for word in words:
        f.write(word + "\n")
