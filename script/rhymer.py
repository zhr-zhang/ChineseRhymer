from word import Word
from character import Character
from typing import List, Callable, Optional
import argparse


class Rhymer:
    words_path = "dependencies/words.txt"
    characters_path = "dependencies/characters.txt"

    def __init__(
        self,
    ):
        print("Loading data...")
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
            Word(word.strip()) for word in words_texts if word.strip()
        ]

    def filter_words(self, conditions: List[Callable[[Word], bool]]) -> List[Word]:
        print("Filtering words...")
        return [
            word
            for word in self.words
            if all(condition(word) for condition in conditions)
        ]

    def length_condition(
        self,
        length: Optional[int] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
    ) -> Callable[[Word], bool]:
        def condition(word: Word) -> bool:
            word_length = len(word.characters)
            if min_length is not None and word_length < min_length:
                return False
            if max_length is not None and word_length > max_length:
                return False
            if length is not None:
                return word_length == length
            return True

        return condition

    def character_condition(
        self, position: int, attribute: str, value: str
    ) -> Callable[[Word], bool]:
        def condition(word: Word) -> bool:
            if position < -len(word.characters) or position >= len(word.characters):
                return False
            return any(
                getattr(pinyin, attribute) == value
                for pinyin in word.characters[position].pinyins
            )

        return condition


def main():
    parser = argparse.ArgumentParser(description="Filter words based on conditions.")
    parser.add_argument("--length", type=int, help="Filter words by exact length.")
    parser.add_argument(
        "--min_length", type=int, help="Filter words by minimum length."
    )
    parser.add_argument(
        "--max_length", type=int, help="Filter words by maximum length."
    )
    parser.add_argument(
        "--position", type=int, help="Position of character for attribute condition."
    )
    parser.add_argument(
        "--attribute",
        type=str,
        help="Character attribute for condition (e.g., vowel, consonant, tone).",
    )
    parser.add_argument(
        "--value", type=str, help="Value of the character attribute for condition."
    )

    args: argparse.Namespace = parser.parse_args()

    rhymer = Rhymer()
    conditions = []

    length = args.length
    min_length = args.min_length
    max_length = args.max_length
    position = args.position
    attribute = args.attribute
    value = args.value

    if length is not None or min_length is not None or max_length is not None:
        if length is not None and (min_length is not None or max_length is not None):
            raise ValueError(
                "Specify either 'length' or 'min_length'/'max_length', but not both."
            )
        conditions.append(
            rhymer.length_condition(
                length=length, min_length=min_length, max_length=max_length
            )
        )

    if position is not None:
        if attribute is None or value is None:
            raise ValueError(
                "Both 'attribute' and 'value' must be specified when using 'position'."
            )
        conditions.append(rhymer.character_condition(position, attribute, value))

    filtered_words = rhymer.filter_words(conditions)
    print(f"{len(filtered_words):4d} words found")
    print(filtered_words)


if __name__ == "__main__":
    main()
