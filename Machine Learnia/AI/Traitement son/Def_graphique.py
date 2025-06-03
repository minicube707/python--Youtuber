import matplotlib.pyplot as plt

def fonction_graphique(x, y, nom_graphique=None, genre=None,
                       x_legend=None, y_legend=None, commentaire=None,
                       color=None, size=None, marker=None, ls=None, lw=None):
    
    #Vérification

    #X Legend
    if x_legend is None:
        x_legend=""

    elif not isinstance(x_legend, str):
        raise ValueError("x_legend doit être un entier")
    

    #Y Legend
    if y_legend is None:
        y_legend=""

    elif not isinstance(y_legend, str):
        raise ValueError("y_legend doit être un entier")
    

    #Nom du graphique
    if nom_graphique is None:
        nom_graphique=""
   

    #Genre de graphique
    if genre is None:
        raise TypeError("Veuillez définir de genre: 'plot', 'scatter'") 
    
    if genre not in ["plot", "scatter"]:
        raise TypeError("Veuillez définir de genre: 'plot', 'scatter'") 
    

    #Type de marquage
    if (marker is None)or(marker=="")or(marker==" "):
        marker=None

    elif not isinstance(marker, list):
        raise TypeError("marker doit être soit un list ou None")
    
    else:
        for element in marker:
            if element not in [None, ".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P", "*", "h", "H", "+", "x", "X", "D", "d", "|", "_"]:
                raise ValueError("Le type de marquage demandait n'est pas disponible")


    #Type de couleur
    if color is None:
        color=None

    elif not isinstance(color, list):
        raise TypeError("color doit être soit un list ou None")
    

    #Ls
    if ls is None:
        ls='-'

    elif not isinstance(ls, list):
        raise TypeError("Ls doit être soit un list ou None")
    

    #Lw
    if lw is None:
        lw=1.5

    elif not isinstance(lw, list):
        raise TypeError("Lw doit être soit un list ou None")

    #Commentaire
    if commentaire is None:
        commentaire=""

    elif not isinstance(commentaire,str):
        raise TypeError ("Le paramètre 'commantaire' doit être un str")


    #Taille
    if size is None:
        size=(6.4, 4.8)  

    elif not isinstance(size, tuple):
        print(type(size))
        raise TypeError("Le paramètre 'size' doit être un tuple")
    
    else:
        if size[0] is None:
            size[0]=6.4
        if size[1] is None:
            size[1]=4.8

    #Atribution des valeus
    size_width=size[0]
    size_height=size[1]
    
    #Graphique
    plt.figure(figsize=(size_width, size_height))
    plt.title(f"{nom_graphique}")
    plt.gcf().set_size_inches(size_width+2, size_height+2)
    plt.figtext(0.5, 0.02, commentaire, fontsize=10, ha='center')

    if genre=="plot":
        plt.plot(x, y, c=color, marker=marker, ls=ls, lw=lw)

    else:
        plt.scatter(x, y, c=color, marker=marker, ls=ls, lw=lw)

    plt.xlabel(f"{x_legend}")
    plt.ylabel(f"{y_legend}")
    plt.show()



def fonction_graphque_comparaison(x_graph, y_graph, nom_graphique=None, genre=None
                                  , x_legend=None, y_legend=None, label_graph=None
                                  , alpha_graph=None,  size=None, commentaire=None
                                  , color=None, marker=None, ls=None, lw=None):
    
    pass_label=False

    #Vérification

    #X et Y
    if not isinstance(x_graph, list) and isinstance(y_graph, list):

        if not isinstance(x_graph, list):
            raise TypeError("Le paramètre 'x_graph' doit être un list")
        
        if not isinstance(y_graph, list):
            raise TypeError("Le paramètre 'y_graph' doit être un list")
        
        
    #X Lengende
    if x_legend is None:
        x_legend=""

    elif not isinstance(x_legend, str):
        raise ValueError("x_legend doit être un texte")
    

    #Y Lengende
    if y_legend is None:
        y_legend=""

    elif not isinstance(y_legend, str):
        raise ValueError("y_legend doit être un  texte")
    

    #Nom du graphique
    if (nom_graphique is None) or (nom_graphique=="default"):
        nom_graphique=""


    #Genre de graphique
    if genre is None:
        raise ValueError("Veuillez définir de genre: 'plot', 'scatter', 'all_plot', 'all_scatter'")
    
    if isinstance(genre, list):

        for element in genre:
            if element not in ["plot", "scatter"]:
                raise ValueError("Veuillez définir de genre: 'plot', 'scatter', 'all_plot', 'all_scatter'")
            
    elif isinstance(genre, str):
        
        if genre == 'all_plot':
            genre=[]
            for _ in range(len(x_graph)):
                genre.append('plot')


        elif genre == 'all_scatter':
            genre=[]
            for _ in range(len(x_graph)):
                genre.append('scatter')

        else:
            raise ValueError("Veuillez définir de genre: 'plot', 'scatter', 'all_plot', 'all_scatter'")
        
    else:
        raise TypeError("genre doit être soit un list ou un str")


    #Type de marquage
    if (marker is None)or(marker=="")or(marker==" "):
        marker=[]

        for _ in range(len(x_graph)):
                marker.append(None)

    elif not isinstance(marker, list):
        raise TypeError("marker doit être soit un list ou None")
    
    else:
        for element in marker:
            if element not in [None, ".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P", "*", "h", "H", "+", "x", "X", "D", "d", "|", "_"]:
                raise ValueError("Le type de marquage demandait n'est pas disponible")


    #Type de couleur
    if color is None:
        color=[]

        for _ in range(len(x_graph)):
            color.append(None)

    elif not isinstance(color, list):
        raise TypeError("color doit être soit un list ou None")
    

    #Ls
    if ls is None:
        ls=[]

        for _ in range(len(x_graph)):
            ls.append('-')

    elif not isinstance(ls, list):
        raise TypeError("Ls doit être soit un list ou None")
    

    #Lw
    if lw is None:
        lw=[]

        for _ in range(len(x_graph)):
            lw.append(1.5)

    elif not isinstance(lw, list):
        raise TypeError("Lw doit être soit un list ou None")

    #Commentaire
    if commentaire is None:
        commentaire=""

    elif not isinstance(commentaire,str):
        raise TypeError ("Le paramètre 'commantaire' doit être un str")


    #Taille
    if size is None:
        size=(6.4, 4.8)

    elif not isinstance(size, tuple):
        print(type(size))
        raise TypeError("Le paramètre 'size' doit être un tuple")


    #Label
    if label_graph is None:
        label_graph=[]
        pass_label=True

        for _ in range(len(x_graph)):
            label_graph.append("")

    elif not isinstance(label_graph, list):
                raise TypeError("Le paramètre 'label_graph' doit être un list")
    

    #Alpha
    if alpha_graph is None:
        alpha_graph=[]

        for _ in range(len(x_graph)):
            alpha_graph.append(1)

    elif not isinstance(alpha_graph, list):
                raise TypeError("Le paramètre 'alpha_graph' doit être un list")

    
    #Atribution des valeurs
    size_width=size[0]
    size_height=size[1]

    #Graphique
    plt.figure(figsize=(size_width,size_height))
    plt.title(nom_graphique)
    plt.gcf().set_size_inches(size_width+2, size_height+2)
    plt.figtext(0.5, 0.02, commentaire, fontsize=10, ha='center')

    for i in range(len(x_graph)):
        if genre[i]=='plot':
            plt.plot(x_graph[i], y_graph[i], label=label_graph[i], alpha=alpha_graph[i], marker=marker[i], c=color[i], ls=ls[i], lw=lw[i])
        if genre[i]=='scatter':
            plt.scatter(x_graph[i], y_graph[i], label=label_graph[i], alpha=alpha_graph[i], marker=marker[i], c=color[i], ls=ls[i], lw=lw[i])

    if pass_label==False:
        plt.legend()

    plt.xlabel(x_legend)
    plt.ylabel(y_legend)
    plt.show()