from collections import OrderedDict


class PinYin:
    CONSONANTS = [
        "b",
        "p",
        "m",
        "f",
        "d",
        "t",
        "n",
        "l",
        "g",
        "k",
        "h",
        "j",
        "q",
        "x",
        "zh",
        "ch",
        "sh",
        "r",
        "z",
        "c",
        "s",
        "y",
        "w",
        "?",
    ]
    VOWELS = [
        "iang",
        "iong",
        "ang",
        "eng",
        "ing",
        "ong",
        "ian",
        "uan",
        "van",
        "uai",
        "iao",
        "ua",
        "an",
        "en",
        "in",
        "un",
        "vn",
        "ai",
        "ei",
        "ui",
        "ao",
        "ou",
        "uo",
        "ia",
        "iu",
        "ie",
        "ve",
        "er",
        "a",
        "o",
        "e",
        "i",
        "!",
        "u",
        "v",
    ]
    HOLISTICS_DICT: OrderedDict = {
        "zhi": "zh!",
        "chi": "ch!",
        "shi": "sh!",
        "ri": "r!",
        "zi": "z!",
        "ci": "c!",
        "si": "s!",
        "yu": "yv",
        "ju": "qv",
        "qu": "qv",
        "xu": "xv",
        "ye": "yie",
        "yang": "yiang",
        "yong": "yiong",
        "yan": "yian",
    }
    TONE_DICT: OrderedDict = {
        "iū": "1",
        "iú": "2",
        "iǔ": "3",
        "iù": "4",
        "iu": "5",
        "uī": "1",
        "uí": "2",
        "uǐ": "3",
        "uì": "4",
        "ui": "5",
        "ā": "1",
        "á": "2",
        "ǎ": "3",
        "à": "4",
        "a": "5",
        "ē": "1",
        "é": "2",
        "ě": "3",
        "è": "4",
        "e": "5",
        "ō": "1",
        "ó": "2",
        "ǒ": "3",
        "ò": "4",
        "o": "5",
        "ǖ": "1",
        "ǘ": "2",
        "ǚ": "3",
        "ǜ": "4",
        "ü": "5",
        "ī": "1",
        "í": "2",
        "ǐ": "3",
        "ì": "4",
        "i": "5",
        "ū": "1",
        "ú": "2",
        "ǔ": "3",
        "ù": "4",
        "u": "5",
    }
    AEIOUV_DICT: OrderedDict = {
        "iū": "iu",
        "iú": "iu",
        "iǔ": "iu",
        "iù": "iu",
        "iu": "iu",
        "uī": "ui",
        "uí": "ui",
        "uǐ": "ui",
        "uì": "ui",
        "ui": "ui",
        "ā": "a",
        "á": "a",
        "ǎ": "a",
        "à": "a",
        "a": "a",
        "ē": "e",
        "é": "e",
        "ě": "e",
        "è": "e",
        "e": "e",
        "ō": "o",
        "ó": "o",
        "ǒ": "o",
        "ò": "o",
        "o": "o",
        "ǖ": "v",
        "ǘ": "v",
        "ǚ": "v",
        "ǜ": "v",
        "ü": "v",
        "ī": "i",
        "í": "i",
        "ǐ": "i",
        "ì": "i",
        "i": "i",
        "ū": "u",
        "ú": "u",
        "ǔ": "u",
        "ù": "u",
        "u": "u",
    }

    def __init__(self, pinyin: str = "zhāng"):
        self.pinyin = pinyin
        self.tone = 0
        self.consonant = ""
        self.vowel = ""

        for key in self.AEIOUV_DICT:
            if key in self.pinyin:
                self.pinyin = self.pinyin.replace(key, self.AEIOUV_DICT[key])
                self.tone = self.TONE_DICT[key]
                break
        for key in self.HOLISTICS_DICT:
            if key in self.pinyin:
                self.pinyin = self.pinyin.replace(key, self.HOLISTICS_DICT[key])
                break
        for vowel in self.VOWELS:
            if vowel in self.pinyin:
                self.vowel = vowel
                self.consonant = self.pinyin.replace(vowel, "")
                if self.consonant == "":
                    self.consonant = "?"
                break

    def __str__(self):
        return f"{self.consonant}{self.vowel}{self.tone}"

    def __repr__(self):
        return f"{self.consonant}{self.vowel}{self.tone}"
