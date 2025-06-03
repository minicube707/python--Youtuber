import random

uppercasse_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowercasse_letter = uppercasse_letter.lower()
digits = "0123456789"
symbole = "&~{}()[]-|_^@=+-*%$,;:.? "

uppers, lowers, nums, syms = True, True, True, True

all = ""

if uppers:
    all += uppercasse_letter

if lowers:
    all += lowercasse_letter

if nums:
    all += digits

if syms:
    all += symbole

lenght = 10
amout  = 20

for _ in range(amout):
    #Choisi au hassard parmi le string all, lenght nombres aléatoires
    password = "".join(random.sample(all, lenght))
    print(password)