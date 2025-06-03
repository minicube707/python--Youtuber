import numpy as np

nb_wagon = int(input("Quelle est le nombre de wagon\n"))
list_arrange = np.arange(nb_wagon)

#Création des wagons
order_wagon = np.array([], dtype=int)
for _ in range(len(list_arrange)):
    rand = np.random.randint(0, len(list_arrange))
    order_wagon = np.append(order_wagon, list_arrange[rand])
    list_arrange = np.delete(list_arrange, rand)
order_wagon += 1

print("Ordre des wagon", order_wagon)

mountain_top = order_wagon.copy()
branch = np.array([], dtype=int)
lake = np.array([], dtype=int)
search_wagon = 1

while search_wagon <= nb_wagon:
    
    print()
    print("Nouveau tour")
    print("lake",lake)
    print("mountain_top", mountain_top)
    print("branch",branch)
    print("")
    if search_wagon in branch:
        print("Le wagon rechercher se trouve à l'embranchement")

        for _ in range(len(branch)):
            if branch[0] == search_wagon:
                print("Wagon trouvé")
                lake = np.append(lake, branch[0])
                branch = np.delete(branch, 0)
                search_wagon +=1
                break

            else:
                print("Déplacement du wagon ", branch[0], " en haut de la montagne")
                mountain_top = np.insert(mountain_top, 0,  branch[0])
                branch = np.delete(branch, 0)
                
    else:
        print("Le wagon rechercher se trouve en haut de la montagne")
        for _ in range(len(mountain_top)):
            if mountain_top[0] == search_wagon:
                print("wagon trouvé")
                lake = np.append(lake, mountain_top[0])
                mountain_top = np.delete(mountain_top, 0)
                search_wagon +=1
                break

            else:
                print("Déplacement du wagon ", mountain_top[0], " à l'embrachement")
                branch = np.insert(branch, 0, mountain_top[0])
                mountain_top = np.delete(mountain_top, 0)
                
print("\nRésultat")        
print("lake",lake)



