from character import Character


class Word:
    def __init__(self, word: str):
        self.word = word
        self.characters = [Character(character) for character in word]
        self.have_polyphone = False
        for character in self.characters:
            if character.is_polyphone:
                self.have_polyphone = True

    def __len__(self):
        return len(self.word)

    def __str__(self):
        return self.word

    def __repr__(self):
        if self.have_polyphone:
            return "*" + self.word
        return self.word


if __name__ == "__main__":
    word = Word("重来")
    print(word)
    print(word.characters)
