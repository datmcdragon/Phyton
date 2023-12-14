from symbol import ascii_chars
from termcolor import colored
import os
import sys
from ASCIIArt import ASCIIArt

class ASCIIArtApp:
    def __init__(self):
        self.run()

    def run(self):
        while True:
            inp_text = input("Type text: ")
            width = int(input("Type width: "))
            height = int(input("Type height: "))

            print("Color:\n1. White\n2. Red")
            selected_color = input("Choose color by number: ")

            art = ASCIIArt(inp_text, width, height, selected_color)
            ascii_art = art.generate()
            print(ascii_art)

            preview_response = input("Want to preview saved ASCII art? (1 - yes, 0 - no): ")
            if preview_response == '1':
                art.save(ascii_art)

            restart_response = input("Do you want to create a new ASCII art? (1 - Yes, 0 - No): ")
            if restart_response != '1':
                break

            os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    app = ASCIIArtApp()
