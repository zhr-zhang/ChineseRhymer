from word import Word
from character import Character
from pinyin import PinYin
from tqdm import tqdm
from typing import Optional, List

words_path = "resource/the_words_i_want.txt"
words_texts = open(words_path, "r", encoding="utf-8").readlines()
words = [Word(word) for word in words_texts if word != ""]
for word in tqdm(words):
    for character in word.characters:
        for pinyin in character.pinyins:
            if pinyin.vowel == "an":
                print(word)
