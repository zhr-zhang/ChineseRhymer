from word import Word
from character import Character
from typing import List, Callable, Optional
from tqdm import tqdm


class Rhymer:
    words_path = "dependencies/words.txt"
    characters_path = "dependencies/characters.txt"

    def __init__(
        self,
    ):
        with open(self.characters_path, "r", encoding="utf-8") as characters_file:
            characters_texts = characters_file.readlines()
        with open(self.words_path, "r", encoding="utf-8") as words_file:
            words_texts = words_file.readlines()
        self.characters: List[Character] = [
            Character(character.strip())
            for character in characters_texts
            if character.strip()
        ]
        self.words: List[Word] = [
            Word(word.strip())
            for word in tqdm(words_texts, desc="Loading words")
            if word.strip()
        ]

    def _select_characters_by_attribute(
        self, attribute: str, value: str
    ) -> List[Character]:
        return [
            character
            for character in self.characters
            if any(getattr(pinyin, attribute) == value for pinyin in character.pinyins)
        ]

    def select_characters_by_consonant(self, consonant: str) -> List[Character]:
        return self._select_characters_by_attribute("consonant", consonant)

    def select_characters_by_vowel(self, vowel: str) -> List[Character]:
        return self._select_characters_by_attribute("vowel", vowel)

    def select_characters_by_tone(self, tone: str) -> List[Character]:
        return self._select_characters_by_attribute("tone", tone)

    def filter_words(self, conditions: List[Callable[[Word], bool]]) -> List[Word]:
        print("Filtering words...")
        filtered_words = self.words
        for condition in conditions:
            filtered_words = [word for word in filtered_words if condition(word)]
        return filtered_words


def nth_character_attribute_condition(
    word: Word, position: int, attribute: str, value: str
) -> bool:
    if position < -len(word.characters) or position >= len(word.characters):
        return False
    return any(
        getattr(pinyin, attribute) == value
        for pinyin in word.characters[position].pinyins
    )


def length_range_condition(
    word: Word,
    length: Optional[int] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
) -> bool:
    word_length = len(word.characters)
    if min_length is not None and word_length < min_length:
        return False
    if max_length is not None and word_length > max_length:
        return False
    if length is not None:
        return word_length == length
    return True


def nth_character_attribute_condition(
    word: Word, position: int, attribute: str, value: str
) -> bool:
    if position < -len(word.characters) or position >= len(word.characters):
        return False
    return any(
        getattr(pinyin, attribute) == value
        for pinyin in word.characters[position].pinyins
    )


if __name__ == "__main__":
    rhymer = Rhymer()
    conditions = [
        # lambda word: length_range_condition(word),
        lambda word: nth_character_attribute_condition(word, -2, "vowel", "ang"),
        lambda word: nth_character_attribute_condition(word, -1, "vowel", "ve"),
        # lambda word: nth_character_attribute_condition(word, -1, "vowel", "ang"),
        # lambda word: nth_character_attribute_condition(word, -3, "tone", "3"),
        # lambda word: nth_character_attribute_condition(word, -2, "tone", "2"),
        # lambda word: nth_character_attribute_condition(word, -1, "tone", "1"),
    ]

    filtered_words = rhymer.filter_words(conditions)
    print(f"{len(filtered_words):4d} words found")
    print(filtered_words)
