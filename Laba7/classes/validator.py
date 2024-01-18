""" Validator file"""
import re

class Validator:
    """Class validator """
    def validate_age(self, age):
        """Перевіряє, чи є вік валідним числом від 0 до 120."""
        try:
            age = int(age)
            return 0 < age < 120
        except ValueError:
            return False

    def validate_color(self, color):
        """Перевіряє, чи є колір в списку допустимих кольорів."""
        allowed_colors = ["blue", "green", "red", "yellow", "pink", "purple", "orange", "black", "white"]
        return color.lower() in allowed_colors

    def validate_hobbie(self, hobbies):
        """Перевіряє, чи є хобі валідним."""
        for hobby in hobbies:
            # A valid hobby should contain only letters (and optionally spaces)
            if not isinstance(hobby, str) or not hobby.replace(" ", "").isalpha():
                return False
        return True

    def validate_email(self, email):
        """Перевіряє, чи введена адреса електронної пошти є валідною."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None
