import json

pinyin_path = "resource/pinyins.txt"

with open(pinyin_path, "r", encoding="utf-8") as f:
    pinyins_texts = f.readlines()

character_pinyin_dict = {}
for text in pinyins_texts:
    parts = pinyin.split(" ")
    character = parts[2]
    pinyin = parts[4]
    character_pinyin_dict[character] = pinyin

# json.dump(
#     character_pinyin_dict,
#     open("dependencies/character_pinyin_dict.json", "w"),
# )
