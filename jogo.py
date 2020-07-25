import random
from sys import exit
from os import stat

FILENAME = "w.txt"
MAX_DAMAGE = 6
STATES = (",----¬\n|\n|\n|\n|\n|",                 # nada
          ",----¬\n|\t o\n|\n|\n|\n|",             # cabeca
          ",----¬\n|\t o\n|\t |\n|\n|\n|",         # corpo
          ",----¬\n|\t o\n|\t/|\n|\n|\n|",         # braço
          ",----¬\n|\t o\n|\t/|\\\n|\n|\n|",
          ",----¬\n|\t o\n|\t/|\\\n|\t/\n|\n|",    # perna
          ",----¬\n|\t o\n|\t/|\\\n|\t/ \\\n|\n|")
VOWELS = ("a", "e", "i", "o", "u")
VARIATIONS = {"a": ("a", "ã", "á"),
              "e": ("e", "é", "ê"),
              "i": ("i", "í"),
              "o": ("o", "ó", "ô"),
              "u": ("u", "ú")
              }


class Word(object):
    def __init__(self, tmp):
        self.formatted = list(tmp)
        self.displayed = []

        for item in self.formatted:
            self.displayed.append("-")

    def vomit_string(self):
        print(*self.displayed)


class Game(object):
    def __init__(self):
        self.word = Word(self.get_word())
        self.damage = 0
        self.guessed = []

    def reset(self):
        self.__init__()

    def get_word(self):
        try:
            file = open(FILENAME, "r", encoding='latin-1')
            words = file.read().splitlines()

            if not words or words == [" "]:
                print("ERRO> lista de palavras vazia")
                file.close()
                exit(1)
            file.close()

            return random.choice(words)
        except OSError:
            print("ERRO> não foi possivel ler a lista de palavras")
            exit(1)

    def display(self):
        print(STATES[self.damage] + "\t", end='')
        self.word.vomit_string()
        print("\n\tjá tentou> ", end=' ')
        print(*self.guessed)

    def endgame(self):
        self.display()
        if self.damage >= MAX_DAMAGE:
            print("game over :(")
        elif self.word.displayed == self.word.formatted:
            print("vitória :)")
        else:
            print("erro")

        print("tentar de novo?")
        print("1-SIM")
        print("2-NÃO")
        a = input(">")

        if int(a) == 1:
            self.reset()
            self.mainloop()

    def insert(self, character):
        for index, letter in enumerate(self.word.formatted):
            if letter == character:
                self.word.displayed[index] = self.word.formatted[index]

    def update_guesses(self, character):
        self.guessed.append(character)

    def compare_vowels(self, character):
        dmg = 1
        for variation in VARIATIONS[character]:
            if variation in self.guessed:
                print("já tentou, pulando")
                dmg = 0
            elif variation in self.word.formatted:
                self.insert(variation)
                dmg = 0
            self.update_guesses(variation)
        return dmg

    def compare(self, character):
        if character in self.guessed:
            print(character + "já tentou, pulando")
        elif character in self.word.formatted:
            for index, letter in enumerate(self.word.formatted):
                if letter == character:
                    self.word.displayed[index] = self.word.formatted[index]
        else:
            self.update_guesses(character)
            return 1
        return 0

    def read_input(self, tmp):
        for item in tmp:
            if item.lower() in VOWELS:
                self.damage += self.compare_vowels(item.lower())
            else:
                self.damage += self.compare(item.lower())

    def mainloop(self):
        while self.damage < MAX_DAMAGE and self.word.displayed != self.word.formatted:
            self.display()
            guess = input("> ")

            self.read_input(guess)

        self.endgame()


random.seed()
game = Game()
game.mainloop()
