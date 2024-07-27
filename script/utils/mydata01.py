from character import Character
from pinyin import PinYin
from typing import List

with open("data/kXHC1983.txt", "r") as f:
    infos = f.readlines()

characters: List[Character] = [Character(info) for info in infos]
usual_character_objects: List[Character] = []
usual_character_list: List[Character] = []
with open("data/usual_list.txt", "r") as f:
    usual_character_list = f.readline().split()

for character in characters:
    if character.character in usual_character_list:
        usual_character_objects.append(character)

with open("data/usual_obj.txt", "w") as f:
    for character in usual_character_objects:
        existing_consonant_and_vowel = []
        for pinyin in character.pinyins:
            f.write(
                f"{character.character} {pinyin.consonant} {pinyin.vowel} {pinyin.tone}\n"
            )

with open("data/usual_vowel.txt", "w") as f:
    for vowel in PinYin.VOWELS:
        f.write(f"{vowel}\n")
        for character in usual_character_objects:
            for pinyin in character.pinyins:
                if pinyin.vowel == vowel:
                    f.write(f"{character.character}")
                    break
        f.write("\n\n")

with open("data/usual_consonant.txt", "w") as f:
    for consonant in PinYin.CONSONANTS:
        f.write(f"{consonant}\n")
        for character in usual_character_objects:
            for pinyin in character.pinyins:
                if pinyin.consonant == consonant:
                    f.write(f"{character.character}")
                    break
        f.write("\n\n")
