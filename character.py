from pinyin import PinYin


class Character:
    def __init__(self, info: str = "4E2D zhōng,zhòng 中"):
        info = info.split()
        self.unicode = info[0]
        self.character = info[2]
        self.pinyins = info[1].split(",")
        self.pinyins = [PinYin(pinyin) for pinyin in self.pinyins]


c = Character("8BAD xùn 训")
print(c.pinyins[0].pinyin)
print(c.pinyins[0].vowel)
print(c.pinyins[0].consonant)
print(c.pinyins[0].tone)
