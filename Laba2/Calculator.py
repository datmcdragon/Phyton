from Memory import Memory
from questions import questions
import math
import gettext
import locale

# Calculator class for performing calculations
class Calculator:
    OPERATORS = {
        '+': lambda num1, num2: num1 + num2,
        '-': lambda num1, num2: num1 - num2,
        '*': lambda num1, num2: num1 * num2,
        '/': lambda num1, num2: num1 / num2 if num2 != 0 else _("Error: division on zero"),
        '^': lambda num1, num2: num1 ** num2,
        '√': lambda num1, _: math.sqrt(num1) if num1 >= 0 else _("Error: negative number under the root"),
        '%': lambda num1, num2: num1 % num2 if num2 != 0 else _("Error: division on zero")
    }

    def __init__(self, locale):
        self.memory = Memory()
        self.locale = locale

    #throws value exception if user input not float numberS
    def get_input(self, prompt_key):
        while True:
            try:
                return float(input(questions[self.locale][prompt_key]))
            except ValueError:
                print(_("Error: Invalid number. Please enter a valid number."))
            

    def run(self):
        while True:
            num1 = self.get_input('first_number')
            num2 = self.get_input('second_number')

            operator = input(questions[self.locale]['operator'])
            if operator in Calculator.OPERATORS:
                result = Calculator.OPERATORS[operator](num1, num2)
                print(_("Result:"), result)
                expression = f"{num1} {operator} {num2}"
                self.memory.store(expression, result)
            else:
                print(_("Error: Invalid operator. Please choose one of these operators: '+, -, *, /, ^, √, %' "))

            memory_values = self.memory.recall()
            print(_("Memory operator:"))
            for expression, result in memory_values:
                print(f"{expression} = {result}")

            repeat = input(questions[self.locale]['continue']).strip().lower()
            if repeat != 'так' and repeat != 'yes':
                break

# Set the default language to Ukrainian
locale.setlocale(locale.LC_ALL, 'uk_UA.utf8')

# Function to choose the language
def choose_language():
    language = input("Оберіть мову | Choose language (укр/eng): ").strip().lower()
    if language == "eng":
        return 'en_US'
    elif language == "укр":
        return 'uk_UA'
    else:
        print("Непідтримувана мова, обрана українська.")
        return 'uk_UA'

# Localization function based on the selected language
selected_locale = choose_language()
_ = gettext.translation('calculator', localedir='locales', languages=[selected_locale], fallback=True).gettext

