from enum import Enum

class Color(Enum):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    PINK = '\033[95m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_in_color(color, text):
    """Prints text in color to the terminal.

    Args:
        color (Color): Color enum
        text (str): Text to print
    """
    color_code = color.value
    reset_code = Color.RESET.value
    print(f"{color_code}{text}{reset_code}")