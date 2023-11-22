from character import Character
from pinyin import PinYin

with open("data/kXHC1983.txt", "r") as f:
    infos = f.readlines()
    f.close()

characters = [Character(info) for info in infos]
usual_character_objects = []
usual_character_list = []
with open("data/usual_list.txt", "r") as f:
    usual_character_list = f.readline().split()
    f.close()

for character in characters:
    if character.character in usual_character_list:
        usual_character_objects.append(character)

with open("data/usual_obj.txt", "w") as f:
    for character in usual_character_objects:
        existing_consonant_and_vowel = []
        for pinyin in character.pinyins:
            if (pinyin.consonant + pinyin.vowel) not in existing_consonant_and_vowel:
                existing_consonant_and_vowel.append(pinyin.consonant + pinyin.vowel)
                f.write(f"{character.character} {pinyin.consonant} {pinyin.vowel}\n")
            else:
                character.pinyins.remove(pinyin)
    f.close()

with open("data/usual_vowel.txt", "w") as f:
    for vowel in PinYin.VOWELS:
        f.write(f"{vowel}\n")
        for character in usual_character_objects:
            for pinyin in character.pinyins:
                if pinyin.vowel == vowel:
                    f.write(f"{character.character}")
                    break
        f.write("\n\n")
    f.close()

with open("data/usual_consonant.txt", "w") as f:
    for consonant in PinYin.CONSONANTS:
        f.write(f"{consonant}\n")
        for character in usual_character_objects:
            for pinyin in character.pinyins:
                if pinyin.consonant == consonant:
                    f.write(f"{character.character}")
                    break
        f.write("\n\n")
    f.close()
