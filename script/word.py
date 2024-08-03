from character import Character
from typing import List, Dict


class Word:
    characters_path = "dependencies/characters.txt"
    str_character_dict: Dict[str, Character] = {}

    @staticmethod
    def load_characters():
        if not Word.str_character_dict:
            with open(Word.characters_path, "r", encoding="utf-8") as characters_file:
                characters_texts = characters_file.readlines()
            Word.str_character_dict = {
                character.strip(): Character(character.strip())
                for character in characters_texts
                if character.strip()
            }

    def __init__(self, word: str):
        Word.load_characters()
        self.word = word
        self.characters = [
            Word.str_character_dict[char]
            for char in word
            if char in Word.str_character_dict
        ]
        self.have_polyphone = any(
            character.is_polyphone for character in self.characters
        )

    def __len__(self):
        return len(self.word)

    def __str__(self):
        return self.word

    def __repr__(self):
        return "*" + self.word if self.have_polyphone else self.word


if __name__ == "__main__":
    Word.load_characters()  # Ensure characters are loaded before creating Word instances
    word = Word("重来")
    print(word)
    print(word.characters)
