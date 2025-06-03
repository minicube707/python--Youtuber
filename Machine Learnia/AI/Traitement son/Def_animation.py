import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def fonction_animation(Tab, freq, répétition, size=None):

    if size ==None:
        size=(6.4, 4.8)
    elif not isinstance(size, tuple):
        print(type(size))
        raise TypeError("Le paramètre doit être un tuple")
    
    #Atribution des valeurs
    size_width=size[0]
    size_height=size[1]

    # Créer la figure et l'axe
    fig, ax = plt.subplots(figsize=(size_width, size_height))
    fig.set_size_inches(10, 8)

    def generate_figure(i, Tab, freq):
        
        if i ==0:
            ax.clear()

        ligne_Y=Tab[i,:]
        x=np.arange(0, Tab.shape[1], 1)

        ax.plot(x, ligne_Y)
        ax.set_title(f'Frame {i}')

        plt.title(f'La fréquence {freq[i,0]} dans le temps')
        plt.xlabel("Time")
        plt.ylabel("Fréquence")

    # Créer l'animation
    animation = FuncAnimation(fig, generate_figure, fargs=(Tab, freq), frames=range(Tab.shape[0]), repeat=répétition)
    # Afficher l'animation
    plt.show()