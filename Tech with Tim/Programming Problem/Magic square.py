import numpy as np

#Création du carré
lenght = int(input("Qu'elle  est la longueur de votre matrice carré\n"))
twoD_matrice = np.array([], dtype=int)


for _ in range(lenght**2):
    number = input("Enter un nombre\n")
    number = int(number)
    twoD_matrice = np.append(twoD_matrice, number)

twoD_matrice = twoD_matrice.reshape((lenght, lenght))

#Affichage du carré
print()
print("Voici la matrice")
for row in twoD_matrice:
    print(row)

#Vérification des propriété
sum = np.sum(twoD_matrice[0,:])
magic_square = True

for i in range(1, lenght):
    new_sum = np.sum(twoD_matrice[i,:])
    if new_sum != sum:
        magic_square = False

if magic_square == True:

    for i in range (lenght):
        new_sum = np.sum(twoD_matrice[:, i])
        if new_sum != sum:
            magic_square = False

if magic_square == True:
    new_sum = 0
    for i in range (lenght):
        new_sum += twoD_matrice[i, i]
    if new_sum != sum:
        magic_square = False

if magic_square == True:
    new_sum = 0
    for i in range (lenght):
        new_sum += twoD_matrice[lenght-i-1, i]
    if new_sum != sum:
        magic_square = False


#Affichage du résultat
if magic_square == True:
    print("Ce carré est magic")

else:
    print("Ce carré n'est magic")