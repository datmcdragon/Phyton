from symbol import ascii_chars
from termcolor import colored
import os
import sys

class ASCIIArt:
    def __init__(self, text, width, height, color):
        self.text = text.upper()
        self.width = width
        self.height = height
        self.color = self.choose_color(color)

    def choose_color(self, color):
        return 'white' if color == '1' else 'red' if color == '2' else 'white'

    def generate(self):
        max_lines = max(len(ascii_chars['A']), *map(len, ascii_chars.values()))
        art = [""] * max_lines

        for char in self.text:
            char_data = ascii_chars.get(char, ascii_chars.get(' ', [' ' * len(ascii_chars['A'])] * len(ascii_chars['A'])))
            for i, line in enumerate(char_data):
                art[i] += colored(line[:self.width] + " " * (self.width - len(line[:self.width])), self.color)
                if len(art) < self.height:
                    art.extend([colored(' ' * self.width, self.color)] * (self.height - len(art)))

        return "\n".join(art[:self.height])

    def save(self, ascii_art):
        with open('figure.txt', 'w') as file:
            file.write(ascii_art)
            print("ASCII-арт збережено у файл 'figure.txt'.")