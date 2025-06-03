import math
import colorama
import time

class PROGRESS_BAR():
    start = time.time()

    def progress_bar(progress, total, color = colorama.Fore.YELLOW):

        #Progression
        percent = (100 * (progress/ float(total)))
        bar = "█" * int(percent) + "-" * (100 - int(percent))

        #Time
        tim = time.time()
        chrono = (tim - PROGRESS_BAR.start)
        end_time = 100 * chrono/percent
        remaning_time = end_time - chrono
        remaning_time_s = remaning_time % 60
        remaning_time_m = remaning_time // 60

        #Affichage
        print(color + f"\r|{bar}| {percent:.2f}%  Min:{remaning_time_m:.0f}  S:{remaning_time_s:.0f}", end="\r")

        if progress == total:
            print(colorama.Fore.GREEN + f"\r|{bar}| {percent:.2f}%  Min:{remaning_time_m:.0f}  S:{remaning_time_s:.0f}", end="\r")
            print(colorama.Fore.RESET)



number = [x * 5 for x in range (1000, 2500)]
result = []

for i, x in enumerate(number):
    result.append(math.factorial(x))
    PROGRESS_BAR.progress_bar(i+1, len(number))
