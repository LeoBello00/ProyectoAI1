def print_red(text):
    print(f"\033[91m{text}\033[00m")

def print_blue(text):
    print(f"\033[94m{text}\033[00m")

def print_colour(text, colour):
    if colour == "red":
        print_red(text)
    elif colour == "blue":
        print_blue(text)
    else:
        print(text)