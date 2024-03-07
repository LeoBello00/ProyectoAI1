def return_text_red(text):
    return f"\033[91m{text}\033[00m"

def return_text_blue(text):
    return f"\033[94m{text}\033[00m"

def return_text_colour(text, colour, end="\n"):
    if colour == 1:
        return return_text_red(text) + end
    elif colour == -1:
        return_text_blue(text) + end
    else:
        return text + end