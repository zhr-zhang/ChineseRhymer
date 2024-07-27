from typing import List

standard_character_paths = [
    "reference/standard_table/level-1.txt",
    "reference/standard_table/level-2.txt",
    "reference/standard_table/level-3.txt",
]
character_path = "resource/characters.txt"
pinyin_path = "resource/kXHC1983.txt"

characters_texts: List[str] = []
for standard_character_path in standard_character_paths:
    with open(character_path, "r") as f:
        characters_texts += f.readlines()
characters = [info.split(",")[2] for info in characters_texts]
with open(pinyin_path, "r") as f:
    infos2 = f.readlines()
characters_with_pinyin = [info.split(" ")[2].replace("\n", "") for info in infos2]

with open(standard_character_paths, "w", encoding="utf-8") as f:
    for character in characters:
        if character in characters_with_pinyin:
            f.write(character + "\n")
