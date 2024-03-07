def return_text_red(text):
    return f"\033[31m{text}\033[0m"

def return_text_blue(text):
    return f"\033[34m{text}\033[0m"

def return_text_colour(text, colour, end="\n"):
    if colour == 1:
        text = return_text_red(text)
    elif colour == -1:
        text = return_text_blue(text)
    return text + end