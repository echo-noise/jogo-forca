import random
from sys import exit
from os import stat
from options import *

class Core(object):
    def __init__(self):
        self.word = list(self.get_word())
        self.damage = 0
        self.maxdamage = 6
        self.guessed = []
        self.found = self.make_enigma() 
    
    def reset(self):
        self.__init__()

    def make_enigma(self):
        l = []
        for item in self.word:
            l.append("0")
        return l

    def solve_enigma(self, character):
        for index, letter in enumerate(self.word):
            if letter == character:
                self.found[index] = self.word[index]

    def get_word(self):
        try:
            file = open(FILENAME, "r", encoding='latin-1')
            words = file.read().splitlines()

            file.close()
            if not words or words == [" "]:
                return 1

            return random.choice(words)
        except OSError:
            return 1
            exit(1)

    def update_guesses(self, guess):
        self.guessed.append(guess)

    def compare_vowels(self, character):
        dmg = 1
        for variation in VARIATIONS[character]:
            if variation in self.guessed:
                dmg = 0
            elif variation in self.word:
                self.solve_enigma(variation)
                dmg = 0
            else:
                self.update_guesses(variation)
        self.damage += dmg

    def compare(self, character):
        if character in self.guessed or character in self.found:
            pass
        elif character in self.word:
            self.solve_enigma(character)
        else:
            self.update_guesses(character)
            self.damage += 1

    def read_input(self, item):
        if item.lower() in VOWELS:
            self.compare_vowels(item.lower())
        else:
            self.compare(item.lower())
                

