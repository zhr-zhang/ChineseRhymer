from pinyin import PinYin
import json
from typing import Dict


class Character:
    character_pinyin_dict_path = "dependencies/character_pinyin_dict.json"
    with open(
        character_pinyin_dict_path, "r", encoding="utf-8"
    ) as character_pinyin_dict_file:
        character_pinyin_dict: Dict[str, str] = json.load(character_pinyin_dict_file)

    def __init__(self, character: str):
        self.character = character.replace("\n", "")
        self.pinyins = self.character_pinyin_dict[self.character].split(",")
        self.is_polyphone = False if len(self.pinyins) == 1 else True
        self.pinyins = [PinYin(pinyin) for pinyin in self.pinyins]

    def __str__(self):
        return self.character

    def __repr__(self):
        return self.character


if __name__ == "__main__":
    c = Character("中")
    print(c.pinyins[0].pinyin)
    print(c.pinyins[0].vowel)
    print(c.pinyins[0].consonant)
    print(c.pinyins[0].tone)
    print(c.is_polyphone)
