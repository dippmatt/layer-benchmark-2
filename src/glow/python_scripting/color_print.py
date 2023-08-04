from enum import Enum

class Color(Enum):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    PINK = '\033[95m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_in_color(color, text):
    color_code = color.value
    reset_code = Color.RESET.value
    print(f"{color_code}{text}{reset_code}")