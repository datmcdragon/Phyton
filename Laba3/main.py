import art
from termcolor import colored

class AsciiArtGenerator:
    def __init__(self):
        self.colors = {
            'червоний': 'red',
            'синій': 'blue',
            'зелений': 'green'
        }

    def get_user_input(self, prompt, default=None):
        user_input = input(prompt).strip()
        return user_input if user_input else default

    def get_art(self, font_name, text):
        try:
            return art.text2art(text, font=font_name)
        except Exception as e:
            print(f"Помилка: {e}")
            return art.text2art(text, font='block')

    def get_color(self):
        color_name = input("Виберіть колір тексту (червоний/синій/зелений): ").lower()
        return self.colors.get(color_name, 'white')

    def get_size(self):
        try:
            width = int(input("Введіть ширину ASCII-арту: "))
            height = int(input("Введіть висоту ASCII-арту: "))
        except ValueError:
            width, height = 80, 20
        return width, height

    def run(self):
        text = self.get_user_input("Введіть слово або фразу для генерації ASCII-арту: ")
        font_name = self.get_user_input("Виберіть шрифт (стандартний/керований/блоки): ", default='block')
        art_object = self.get_art(font_name, text)
        color = self.get_color()
        width, height = self.get_size()
        char = self.get_user_input("Введіть символ, який ви хочете використовувати (наприклад, '@', '#', '*'): ")

        colored_art = colored(art_object, color)
        print("Попередній перегляд вашого ASCII-арту:")
        formatted_art = colored_art.center(width).replace(' ', char)
        print(formatted_art)

        save_option = input("Зберегти ASCII-арт у файл? (так/ні): ").lower()
        if save_option == 'так':
            file_name = input("Введіть ім'я файлу для збереження: ")
            with open(file_name, 'w') as file:
                file.write(formatted_art)
                print(f"ASCII-арт був збережений у файлі '{file_name}'")

        print("Дякуємо за використання нашого генератора ASCII-арту!")

if __name__ == "__main__":
    generator = AsciiArtGenerator()
    generator.run()
