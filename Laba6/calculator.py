import math
import gettext
import locale

# Memory class for storing user inputs and results
class Memory:
    def __init__(self):
        self.memory = []

    def store(self, expression, result):
        self.memory.append((expression, result))

    def recall(self):
        return self.memory

    def clear(self):
        self.memory = []

# Calculator class for performing calculations
class Calculator:
    OPERATORS = {
        '+': lambda num1, num2: num1 + num2,
        '-': lambda num1, num2: num1 - num2,
        '*': lambda num1, num2: num1 * num2,
        '/': lambda num1, num2: num1 / num2 if num2 != 0 else _("Error: division on zero"),
        '^': lambda num1, num2: num1 ** num2,
        '√': lambda num1, _: math.sqrt(num1) if num1 >= 0 else "Error: negative number under the root",
        '%': lambda num1, num2: num1 % num2 if num2 != 0 else _("Error: division on zero")
    }

    def __init__(self, locale):
        self.memory = Memory()
        self.locale = locale

    def get_float_input(self, prompt_key):
        while True:
            try:
                return float(input(questions[self.locale][prompt_key]))
            except ValueError:
                print(_("Error: Invalid input, please enter a valid number."))

    def run(self):
        while True:
            num1 = self.get_float_input('first_number')
            num2 = self.get_float_input('second_number')

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

# Dictionary for localized prompts and messages
questions = {
    'en_US': {
        'first_number': "First number: ",
        'second_number': "Second number: ",
        'operator': "Choose operator (+, -, *, /, ^, √, %): ",
        'continue': "Do you want to continue? (yes/no): "
    },
    'uk_UA': {
        'first_number': "Перше число: ",
        'second_number': "Друге число: ",
        'operator': "Оберіть операцію (+, -, *, /, ^, √, %): ",
        'continue': "Бажаєте продовжити? (так/ні): "
    }
}

if __name__ == "__main__":
    calculator = Calculator(selected_locale)
    calculator.run()
