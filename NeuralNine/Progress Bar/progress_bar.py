import math
import colorama
import time

def progress_bar(progress, total, color = colorama.Fore.YELLOW):
    percent = (100 * (progress/ float(total)))
    bar = "█" * int(percent) + "-" * (100- int(percent))
    chrono = time.time()
    print(color + f"\r|{bar}| {percent:.2f}%", end="\r")
    if progress == total:
        print(colorama.Fore.GREEN + f"\r|{bar}| {percent:.2f}%", end="\r")
        print(colorama.Fore.RESET)



number = [x * 5 for x in range (2000, 3000)]
result = []

for i, x in enumerate(number):
    result.append(math.factorial(x))
    progress_bar(i+1, len(number))
