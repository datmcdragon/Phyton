import math

# Class to track user calculations
class CalculationTracker:
    def __init__(self):
        self.history = []

    def add_record(self, expr, res):
        self.history.append((expr, res))

    def get_history(self):
        return self.history

    def reset_history(self):
        self.history = []

def perform_calculation(a, b, op):
    operations = {
        '+': lambda: a + b,
        '-': lambda: a - b,
        '*': lambda: a * b,
        '/': lambda: a / b if b != 0 else "Error: Division by zero",
        '^': lambda: a ** b,
        '√': lambda: math.sqrt(a) if a >= 0 else "Error: Square root of negative number",
        '%': lambda: a % b if b != 0 else "Error: Modulo by zero"
    }

    func = operations.get(op)
    if not func:
        return "Error: Unknown operator. Please try again."

    try:
        return func()
    except ZeroDivisionError:
        return "Error: Division by zero"
    except ValueError:
        return "Error: Invalid input"

calc_tracker = CalculationTracker()

while True:
    try:
        first_num = float(input("Enter the first number: "))
        second_num = float(input("Enter the second number: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    while True:
        operation = input("Operator (+, -, *, /, ^, √, %): ")
        if operation in ['+', '-', '*', '/', '^', '√', '%']:
            outcome = perform_calculation(first_num, second_num, operation)
            print(f"Result: {outcome}")
            calc_tracker.add_record(f"{first_num} {operation} {second_num}", outcome)
            break
        else:
            print("Invalid operator. Choose from +, -, *, /, ^, √, %.")

    print("Calculation History:")
    for expr, res in calc_tracker.get_history():
        print(f"{expr} = {res}")

    if input("Continue? (yes/no): ").lower() != 'yes':
        break
