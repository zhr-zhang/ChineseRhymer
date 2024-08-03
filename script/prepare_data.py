import re
from typing import List, Dict

# from tqdm import tqdm
import json
import os

# 定义文件路径
standard_character_files = [
    "resource/standard_characters/level-1.txt",
    "resource/standard_characters/level-2.txt",
    "resource/standard_characters/level-3.txt",
]
simple_word_files = [
    "resource/words_data/中文分词词库整理/dict.txt",
    "resource/words_data/中文分词词库整理/fingerDic.txt",
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
thuocl_word_files = [
    "resource/words_data/动物词库/THUOCL_animal.txt",
    "resource/words_data/医学词库/THUOCL_medical.txt",
    "resource/words_data/成语词库/THUOCL_chengyu.txt",
    "resource/words_data/法律词库/THUOCL_law.txt",
    "resource/words_data/财经词库/THUOCL_caijing.txt",
    "resource/words_data/食物词库/THUOCL_food.txt",
    "resource/words_data/中文分词词库整理/四十万可用搜狗txt词库.txt",
]
dependencies_dir = "dependencies"
characters_output_path = "dependencies/characters.txt"
character_pinyin_dict_path = "dependencies/character_pinyin_dict.json"
words_output_path = "dependencies/words.txt"

# 准备标准字符集
print("Preparing characters...")
standard_characters: List[str] = []
for file_path in standard_character_files:
    with open(file_path, "r", encoding="utf-8") as f:
        standard_characters.extend(f.readlines())
standard_characters_set = set(
    info.strip().split(",")[2] for info in standard_characters
)

# 准备拼音字典
print("Preparing pinyins...")
character_pinyin_dict: Dict[str, str] = {}

with open("resource/pinyin.txt", "r", encoding="utf-8") as f:
    pinyin_lines = f.readlines()
for line in pinyin_lines:
    parts = line.strip().split(" ")
    character = parts[2]
    pinyin = parts[1]
    if character in standard_characters_set:
        if character in character_pinyin_dict:
            character_pinyin_dict[character] += "," + pinyin
        else:
            character_pinyin_dict[character] = pinyin


# 过滤包含标准字符的词汇
def filter_words_with_standard_characters(words: List[str]) -> List[str]:
    print("Filtering words with standard characters...")
    return [
        word
        for word in words
        if all(character in character_pinyin_dict for character in word)
    ]


# 准备词汇列表
def prepare_words() -> List[str]:
    print("Preparing words...")
    words: List[str] = []
    for file_path in simple_word_files:
        with open(file_path, "r", encoding="utf-8") as f:
            words.extend(word.strip() for word in f.readlines())
    for file_path in thuocl_word_files:
        with open(file_path, "r", encoding="utf-8") as f:
            words.extend(line.split(" ")[0].strip() for line in f.readlines())
    with open(
        "resource/words_data/中文分词词库整理/42537条伪原创词库.txt",
        "r",
        encoding="utf-8",
    ) as f:
        for line in f.readlines():
            words.extend(word.strip() for word in line.split("→"))
    with open("resource/XDHYCD7th.txt", "r", encoding="utf-8") as f:
        xhzd = f.read()
        matches = re.findall(r"【(.*?)】", xhzd)
        words.extend(re.sub(r"（儿）", "", match) for match in matches)
    print("Filtering duplicates...")
    words = list(set(words))
    return filter_words_with_standard_characters(words)


# 写入文件
words = prepare_words()
print("Writing files...")
os.makedirs(dependencies_dir, exist_ok=True)
with open(characters_output_path, "w", encoding="utf-8") as f:
    for character in character_pinyin_dict:
        f.write(character + "\n")
with open(character_pinyin_dict_path, "w", encoding="utf-8") as f:
    json.dump(character_pinyin_dict, f, ensure_ascii=False, indent=4)
with open(words_output_path, "w", encoding="utf-8") as f:
    for word in words:
        f.write(word + "\n")
print(f"Total words: {len(words)}")
