import colorama
import os
from colorama import Fore

r = Fore.RED
g = Fore.GREEN
y = Fore.YELLOW
w = Fore.WHITE



#--------- Start ----------#
def purpleblue(text):
    os.system(""); faded = ""
    red = 110
    for line in text.splitlines():
        faded += (f"\033[38;2;{red};0;255m{line}\033[0m\n")
        if not red == 0:
            red -= 15
            if red < 0:
                red = 0
    return faded
# Creds to https://github.com/venaxyt/fade/blob/main/fade/__init__.py
# For graidients
#------------ End --------------#



# How to use Gradify
# gradify('INFO', option='magenta_to_blue')
# EXAMPLE PRINT FUNCTION
# for this project it would be this 
# print(f"[ {datetime.now()} ] - [{gradify('INFO', option='magenta_to_blue')}] - Webhook profile updated successfully for {webhook}")

def gradify(text, option="magenta_to_blue"):
    
    gradifys = {
        "magenta_to_blue": ((255, 0, 255), (0, 0, 255)),
        "red_to_yellow": ((255, 0, 0), (255, 255, 0)),
        "green_to_cyan": ((0, 255, 0), (0, 255, 255)),
        "blue_to_white": ((0, 0, 255), (255, 255, 255)),
        "rainbow": [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)],
    }

    def interpolate(start, end, factor):
        return int(start + (end - start) * factor)

    if option not in gradifys:
        raise ValueError(f"Invalid gradify option: {option}. Available options: {list(gradifys.keys())}")

    if option == "rainbow":
        # Special case for rainbow gradify
        colors = gradifys["rainbow"]
        result = ""
        length = len(text)
        for i, char in enumerate(text):
            color_index = int(i / length * len(colors)) % len(colors)
            r, g, b = colors[color_index]
            result += f"\033[38;2;{r};{g};{b}m{char}"
        result += "\033[0m"  
        return result

    start_color, end_color = gradifys[option]
    result = ""
    length = len(text)
    for i, char in enumerate(text):
        factor = i / (length - 1) if length > 1 else 0
        r = interpolate(start_color[0], end_color[0], factor)
        g = interpolate(start_color[1], end_color[1], factor)
        b = interpolate(start_color[2], end_color[2], factor)
        result += f"\033[38;2;{r};{g};{b}m{char}"
    result += "\033[0m" 
    return result

