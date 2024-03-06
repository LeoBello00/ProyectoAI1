def print_red(text, end="\n"):
    print(f"\033[91m{text}\033[00m", end=end)

def print_blue(text, end="\n"):
    print(f"\033[94m{text}\033[00m", end=end)

def print_colour(text, colour, end="\n"):
    if colour == 1:
        print_red(text)
    elif colour == -1:
        print_blue(text)
    else:
        print(text)