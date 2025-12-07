import matplotlib.pyplot as plt
import numpy as np


from scipy.signal import argrelextrema 
from scipy.io import wavfile
from scipy.signal import spectrogram
from scipy.signal import istft
from scipy.io.wavfile import write

from Def_graphique import fonction_graphique, fonction_graphque_comparaison
from Def_animation import fonction_animation

from Def_preprocessing3 import function_difference_tangente, normalize_to_range, function_difference_horizon, fonction_trouver_max_plus_grand
from Def_preprocessing3 import fonction_trouver_min_plus_petit, fonction_smooth

from Def_clustering import fonction_clustering_KMeans, fonction_clustering_AffinityPropagation, fonction_clustering_Spectral

import warnings
import os 

def find_indice(matrice, val, axis, indice): #A partir d'une matrice, d'une valeur comprise dans la matrice, de l'indice de la valeur et l'axe de l'indice. #Retourne l'autre indice de l'autre axe
    if axis == 0:
        try:
            i = np.where(matrice[:, indice] == val)[0][0]
        except IndexError:
            i = -1
    elif axis == 1:
        try:
            i = np.where(matrice[indice, :] == val)[0][0]
        except IndexError:
            i = -1
    else:
        raise ValueError("axis doit être compris entre 0 et 1")

    return i
      

# Ignorer les UserWarnings
warnings.filterwarnings("ignore", category=UserWarning)


#Déplacement dans l'ordi
os.chdir("Music\Fichier wav")


#Chargez le contenu du fichier .wav.

#Fichier stéréo:
#5000.wav
#Hvitserk's choice (Deluxe).wav
#My Time 10.wav


fichier_audio="My Time 10.wav"
print("\nfichier audio étudier:",fichier_audio)
sample_rate, audio_data = wavfile.read(fichier_audio)


#La fréquence d'échantillonnage du fichier audio, qui représente le nombre d'échantillons sonores pris par seconde.
#Cette valeur est un entier.
print("")
print("sample_rate=",sample_rate) 


# Les données audio du fichier WAV, stockées sous forme d'un tableau NumPy 
#(un tableau NumPy est essentiellement une structure de données similaire à une liste, mais optimisée pour le calcul numérique).
#Les échantillons audio sont stockés sous forme d'entiers ou de nombres à virgule flottante, en fonction de la précision du fichier WAV.

print("")
print("audio_data=",audio_data.shape)
print(audio_data)
"""
plt.figure()
plt.plot(np.arange(audio_data.shape[0]), audio_data[:, 0], label='Canal Gauche')
plt.plot(np.arange(audio_data.shape[0]), audio_data[:, 1], label='Canal Droite')
plt.xlabel('Échantillons')
plt.ylabel('Amplitude')
plt.title('Signal Audio - Canaux Gauche et Droit')
plt.legend()
plt.show()
"""
print("")
print(f"number of channels of stereo= {audio_data.shape[1]}")
#number of channels = 2

length = audio_data.shape[0] / sample_rate
print("")
print(f"length = {length}s")


#Tracez la forme d’onde.
time = np.linspace(0., length, audio_data.shape[0])
"""
x_graph=[time,time]
y_graph=[audio_data[:,0], audio_data[:,1]]
label=[ "Left channel", "Right channel"]
alpha=[0.7, 0.7]

fonction_graphque_comparaison( x_graph, y_graph, f'Analyse de fichier: {fichier_audio}', genre="all_plot", x_legend="Time [s]"
                              , y_legend="Amplitude", label_graph=label, alpha_graph=alpha)
"""

# Convertir les échantillons en valeurs d'amplitude réelle
amplitude = np.abs(audio_data)


# Calculer l'amplitude en dB
amplitude_db = 20 * np.log10(amplitude)

"""
#Tracez la forme d’onde en db.
x_graph=[time,time]
y_graph=[amplitude_db[:,0],  amplitude_db[:,1]]
label=[ "Left channel", "Right channel"]
alpha=[0.7, 0.7]

fonction_graphque_comparaison( x_graph, y_graph, f'Analyse de fichier: {fichier_audio}', x_legend="Time [s]"
                              , y_legend="Amplitude", genre=['plot', 'plot'], label_graph=label, alpha_graph=alpha)
"""

#Ficheir mono:
#My Time 10_mono.wav
#5000 mono.wav
#Hvitserk's choice (Deluxe) mono.wav


# Read the wav file (mono)
fichier_audio_mono="My Time 10_mono.wav"
sample_rate_mono, audio_data_mono =wavfile.read(fichier_audio_mono)

print("\nfichier audio étudier:",fichier_audio_mono)

audio_data_dim=audio_data_mono.reshape(audio_data_mono.shape[0],1)

print("")
print(f"number of channels of mono = {audio_data_dim.shape[1]}")
#number of channels = 1

print("")
print("audio_data=",audio_data_mono.shape)
print(audio_data_mono)

length_mono = audio_data_mono.shape[0] / sample_rate_mono
time_mono = np.linspace(0., length_mono, audio_data_mono.shape[0])

"""
# Plot the signal read from wav file
plt.figure(figsize=(12,8))
plt.subplot(211)
plt.title(f'Spectrogram of {fichier_audio_mono}')
plt.plot(time_mono, audio_data_mono)
plt.xlabel('Sample')
plt.ylabel('Amplitude')

plt.subplot(212)
plt.specgram(audio_data_mono, Fs=sample_rate_mono)
plt.xlabel('Time[s]')
plt.ylabel('Frequency en Hz')
plt.colorbar(label='Amplitude (dB)')
plt.show()
"""


# Appliquer la transformée de Fourier
frequencies = np.fft.fftfreq(len(audio_data_mono), 1/sample_rate_mono)
fft_values = np.fft.fft(audio_data_mono)

# Ignorer les fréquences négatives (partie miroir dans le spectre)
positive_frequencies = frequencies[:len(frequencies)//2]
positive_fft_values = 2.0/len(audio_data_mono) * np.abs(fft_values[:len(frequencies)//2])
"""
# Afficher le spectre de fréquences
plt.plot(positive_frequencies, positive_fft_values)
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Amplitude')
plt.title('Spectre de fréquences')
plt.show()
"""

# Paramètres de la STFT
nperseg = 2048  # Taille de la fenêtre pour chaque segment temporel
noverlap = 2000  # Nombre d'échantillons de chevauchement entre les segments

# Calcul de la STFT
frequencies, times, Pxx = spectrogram(audio_data_mono, sample_rate_mono, nperseg=nperseg, noverlap=noverlap)

"""
# Afficher le spectrogramme
plt.pcolormesh(times, frequencies, 10 * np.log10(Pxx), shading='auto')
plt.ylabel('Fréquence (Hz)')
plt.xlabel('Temps (s)')
plt.title('Spectrogramme')
plt.colorbar(label='Puissance (dB)')
plt.show()
"""


_, signal_reconstructed = istft(Pxx, window='hann', nperseg=nperseg, noverlap=noverlap)


print("\nSignal.shape:", signal_reconstructed.shape)
print("Signal:\n", signal_reconstructed)
"""
X=[np.arange(signal_reconstructed.size), np.arange(audio_data_mono.size)]
Y=[signal_reconstructed, audio_data_mono]
fonction_graphque_comparaison(X,Y, genre='all_plot', label_graph=["Signal reconstruit", "Signal original"])
"""


# Assumez que signal soit votre signal audio et sample_rate votre taux d'échantillonnage
sample_rate = sample_rate_mono  # Remplacez cela par votre taux d'échantillonnage réel
signal = signal_reconstructed  # Remplacez cela par votre signal réel

# Normalisez le signal à la plage appropriée pour le format WAV (par exemple, int16)
signal_normalized = (signal / np.max(np.abs(signal)) * 32767).astype(np.int16)

# Spécifiez le chemin du fichier WAV de sortie
output_path = 'output.wav'

# Écrivez le fichier WAV
#write(output_path, sample_rate, signal_normalized)



# Assumez que signal soit votre signal audio et sample_rate votre taux d'échantillonnage
sample_rate = sample_rate_mono  # Remplacez cela par votre taux d'échantillonnage réel
origianl_signal = audio_data_mono  # Remplacez cela par votre signal réel

# Normalisez le signal à la plage appropriée pour le format WAV (par exemple, int16)
signal_normalized = (origianl_signal / np.max(np.abs(origianl_signal)) * 32767).astype(np.int16)

# Spécifiez le chemin du fichier WAV de sortie
output_path = 'output_original.wav'

# Écrivez le fichier WAV
#write(output_path, sample_rate, signal_normalized)

print("\nPxx.shape",Pxx.shape)
print("Pxx.size",Pxx.size)
print("Pxx",Pxx)

Pxx = Pxx[np.var(Pxx, axis=1)>0]

print("\nPxx.shape",Pxx.shape)
print("Pxx.size",Pxx.size)
print("Pxx",Pxx)

#Fréquence avec amplitude max pour chaque colonne
amplitude_max = np.max(Pxx, axis=0)
amplitude_min = np.min(Pxx, axis=0)
amplitude_var = Pxx.var(axis=0)
amplitude_mean = Pxx.mean(axis=0)
amplitude_std = Pxx.std(axis=0)

frequence_max = np.max(Pxx, axis=1)
frequence_var = np.var(Pxx, axis=1)
frequence_std = np.std(Pxx, axis=1)
frequence_mean = np.mean(Pxx, axis=1)

n = np.arange(0, amplitude_max.size, 1)

amplitude_max = np.append(amplitude_max, 0)
n = np.append(n, n[-1]+1)

m = np.arange(0, frequence_max.size, 1)


print("\namplitude_max.shape",amplitude_max.shape)
print("amplitude_max.size",amplitude_max.size)
print("amplitude_max",amplitude_max)
"""
print("\nfrequence_max.shape",frequence_max.shape)
print("frequence_max.size",frequence_max.size)
print("frequence_max",frequence_max)
"""
# Trouvez les indices des minimums locaux
minima_indices = argrelextrema(amplitude_max, np.less)
minima_indices = list(minima_indices)
minima_indices = minima_indices[0]

print("\nminima_indices.shape", minima_indices.shape)
print("minima_indices.size", minima_indices.size)


# Trouvez les indices des maximums locaux
maxima_indices = argrelextrema(amplitude_max, np.greater)
maxima_indices = list(maxima_indices)
maxima_indices = maxima_indices[0]

print("\nmaxima_indices.shape", maxima_indices.shape)
print("maxima_indices.size", maxima_indices.size)

                                   
#Boolean indexing pour retirer les valeurs <1
new_inidice_maxima = n[maxima_indices][amplitude_max[maxima_indices]>1]
new_inidice_minima = n[minima_indices][amplitude_max[minima_indices]>1]


#Ajout du 0 étant que dernière valeur minimal retiré
first_indice_minima=n[minima_indices][amplitude_max[minima_indices]<1][-1:]
new_inidice_minima = np.insert(new_inidice_minima, 0, first_indice_minima)

if new_inidice_minima.size > new_inidice_maxima.size:
    new_inidice_maxima = np.append(new_inidice_maxima, n[-1])

print("\nnew_inidice_maxima.shape",new_inidice_maxima.shape)
print("new_inidice_maxima.size", new_inidice_maxima.size)


print("\nnew_inidice_minima.shape",new_inidice_minima.shape)
print("new_inidice_minima.size", new_inidice_minima.size)


#np.savetxt('Data.txt', amplitude_max)
#np.savetxt('Max.txt', new_inidice_maxima)
#np.savetxt('Min.txt', new_inidice_minima)

new_n, new_amplitude_max, masque = function_difference_horizon(new_inidice_minima, new_inidice_maxima, n, amplitude_max, 0.1)

new_amplitude_max = np.append(new_amplitude_max, amplitude_max[-1])
new_n = np.append(new_n, n.size-1)

masque_even = masque[0::2]
masque_odd = masque[1::2]

X=[n, new_n]
Y=[amplitude_max, new_amplitude_max]
fonction_graphque_comparaison(X, Y, genre="all_plot", label_graph=["Fichier originalFichier original", "Preprocesing N°1"], nom_graphique="Premier traitement")

fonction_graphique(new_n, new_amplitude_max, genre="plot", nom_graphique="Premier traitement")


min = np.arange(new_n.size)[0:-1:2]
max = np.arange(new_n.size)[1::2]

print("")
print("min.size",min.size)
print("min",min)

print("")
print("max.size",max.size)
print("max",max)

N, NA, M = function_difference_tangente(min, max, new_n, new_amplitude_max, 0.6)

print("")
print("N.size",N.size)
print("N",N)

print("")
print("NA.size",NA.size)
print("NA",NA)

MIN = argrelextrema(NA, np.less)
MAX = argrelextrema(NA, np.greater)
MIN = MIN[0]
MAX = MAX[0]

MIN = np.insert(MIN, 0, 0)
#MAX = np.append(MAX, N.size-2)

MIN = np.append(MIN, N.size-1)

print("")
print("MIN.size",MIN.size)
print("MIN",MIN)

print("")
print("MAX.size",MAX.size)
print("MAX",MAX)

X=[new_n, N]
Y=[new_amplitude_max, NA]
fonction_graphque_comparaison(X, Y, genre="all_plot", label_graph=["Preprocesing N°1", "Preprocesing N°2"], nom_graphique="Deuxième traitement")

X=[n, N]
Y=[amplitude_max, NA]
fonction_graphque_comparaison(X, Y, genre="all_plot", label_graph=["Fichier original", "Preprocesing N°2"], nom_graphique="Deuxième traitement")

X=[N[MAX], N[MIN], N]
Y=[NA[MAX], NA[MIN], NA]
fonction_graphque_comparaison(X, Y, genre=["scatter","scatter", "plot"], label_graph=["MAX","MIN", "ORI"], nom_graphique="TEST")

fonction_graphique(N, NA, genre="plot", nom_graphique="Deuxième traitement")



N2, NA2, MIN2, MAX2 = fonction_smooth(MIN, MAX, N, NA)

print("")
print("N2.shape",N2.shape)
print("N2.size",N2.size)
print("N2",N2)

print("")
print("NA2.shape",NA2.shape)
print("NA2.size",NA2.size)
print("NA2",NA2)

print("")
print("MIN2.shape",MIN2.shape)
print("MIN2.size",MIN2.size)
print("MIN2",MIN2)

print("")
print("MAX2.shape",MAX2.shape)
print("MAX2.size",MAX2.size)
print("MAX2",MAX2)

plt.figure()
plt.plot(N, NA, label="P2")
plt.plot(N2, NA2, label="P3", linewidth=2.5)
plt.legend()
plt.show()

plt.figure()
plt.scatter(N2[MAX2], NA2[MAX2], label="MAX", s=100)
plt.scatter(N2[MIN2], NA2[MIN2], label="MIN", s=100)
plt.scatter(N2, NA2, label="point")
plt.plot(N2, NA2, label="P3", linewidth=2.5)
plt.legend()
plt.show()

#Modification des max
list_dico_max = fonction_trouver_max_plus_grand(amplitude_max, NA2[MAX2], N2[MAX2])

NEW_MAX = np.array([])
NEW_MAX_INDICE = np.array([])

print("")
for i in range(len(list_dico_max)):

    dico_max =list_dico_max[i]
    print("dico_max",dico_max)

    if dico_max["max_plus_grand_present"] ==  True:
        new_valeur = dico_max.get("max_plus_grand_valeur")
        new_indice = dico_max.get("max_plus_grand_indice")

        NEW_MAX = np.append(NEW_MAX, new_valeur)
        NEW_MAX_INDICE =  np.append(NEW_MAX_INDICE, new_indice)

    else:
        NEW_MAX = np.append(NEW_MAX, NA2[MAX2][i])
        NEW_MAX_INDICE = np.append(NEW_MAX_INDICE, N2[MAX2][i])

print("")
print("NEW_MAX.size",NEW_MAX.size)
print("NEW_MAX",NEW_MAX)

print("")
print("NEW_MAX_INDICE.size",NEW_MAX_INDICE.size)
print("NEW_MAX_INDICE",NEW_MAX_INDICE)


#Affichage des min
list_dico_min = fonction_trouver_min_plus_petit(amplitude_max, NA2[MIN2], N2[MIN2])

NEW_MIN = np.array([])
NEW_MIN_INDICE = np.array([])

print("")
for i in range(len(list_dico_min)):

    dico_min =list_dico_min[i]
    print("dico_min",dico_min)

    if dico_min["min_plus_petit_present"] ==  True:
        new_valeur = dico_min.get("min_plus_petit_valeur")
        new_indice = dico_min.get("min_plus_petit_indice")

        NEW_MIN = np.append(NEW_MIN, new_valeur)
        NEW_MIN_INDICE =  np.append(NEW_MIN_INDICE, new_indice)

    else:
        NEW_MIN = np.append(NEW_MIN, NA2[MIN2][i])
        NEW_MIN_INDICE = np.append(NEW_MIN_INDICE, N2[MIN2][i])

print("")
print("NEW_MIN.size",NEW_MIN.size)
print("NEW_MIN",NEW_MIN)

print("")
print("NEW_MIN_INDICE.size",NEW_MIN_INDICE.size)
print("NEW_MIN_INDICE",NEW_MIN_INDICE)


NEW_NA = NA2.copy()
NEW_N = N2.copy()

NEW_NA[MAX2] = NEW_MAX
NEW_N[MAX2] = NEW_MAX_INDICE

NEW_NA[MIN2] = NEW_MIN
NEW_N[MIN2] = NEW_MIN_INDICE

print("")
print("NEW_NA.size",NEW_NA.size)
print("NEW_NA",NEW_NA)

print("")
print("NEW_N.size",NEW_N.size)
print("NEW_N",NEW_N)

X=[NEW_N, N]
Y=[NEW_NA, NA]
fonction_graphque_comparaison(X, Y, genre="all_plot", label_graph=["Preprocesing N°3", "Preprocesing N°2"], nom_graphique="Troisième traitement")

fonction_graphique(NEW_N, NEW_NA, genre="plot", nom_graphique="Troisième traitement")

#Affichage des repères max
X1=[]
X2=[]
X3=[]
X4=[]

for i in range(len(MIN)):
      X1.append(NEW_NA[MIN][i] - NEW_NA[MAX][i])
      X2.append(NEW_N[MIN][i] - NEW_N[MAX][i])
      X3.append(NEW_NA[MAX][i])
      d = find_indice(Pxx, NEW_NA[MAX][i], 0, NEW_N[MAX][i])
      X4.append(d)


print("\nX1.shape",len(X1))
print("X1",X1)
X1_nor = normalize_to_range(X1, -1, 1)
print("X1_nor",X1_nor)

print("\nX2.shape",len(X2))
print("X2",X2)
X2_nor = normalize_to_range(X2, -1, 1)
print("X2_nor",X2_nor)

print("\nX3.shape",len(X3))
print("X3",X3)
X3_nor = normalize_to_range(X3, -1, 1)
print("X3_nor",X3_nor)

print("\nX4.shape",len(X4))
print("X4",X4)
X4_nor = normalize_to_range(X4, -1, 1)
print("X4_nor",X4_nor)

X  = np.column_stack((X1_nor, X2_nor, X3_nor, X4_nor))

print("")
print("X",X)


"""///////////////////////////////////////////////"""
"""K Mean"""


print("")
print("K Mean")
cluster, label = fonction_clustering_KMeans(X, 10)

#Affichage des données
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(X[:,0], X[:,1], X[:,2], c=label, marker='o', label="Data")
ax.scatter(cluster[:,0], cluster[:,1], cluster[:,2], c='r', marker='+', label="Cluster")

ax.set_xlabel('Différence des ordonnées')
ax.set_ylabel('Différence des abscisses')
ax.set_zlabel('Ordonnées')
ax.legend()
plt.show()


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(X[:,1], X[:,2], X[:,3], c=label, marker='o', label="Data")
ax.scatter(cluster[:,1], cluster[:,2], cluster[:,3], c='r', marker='+', label="Cluster")

ax.set_xlabel('Différence des ordonnées')
ax.set_ylabel('Différence des abscisses')
ax.set_zlabel('Ordonnées')
ax.legend()
plt.show()

print("\ncluster:\n",cluster)
print("\nlabel",label)

nb_label, size_nb = np.unique(label, return_counts=True)

print("")
print("nb_label",nb_label)
print("size_nb",size_nb)

print("")
# Afficher les éléments uniques et leur comptage
for element, compteur in zip(nb_label, size_nb):
    print(f"Élément {element} : {compteur} occurrences")


"""//////////////////////////"""

print("")
print("Affichage des données")

plt.figure()
plt.title(f"Final point with Max Final point: point={N[MAX][:-1].size}")
plt.scatter( NEW_N[MAX], NEW_NA[MAX], c=label)
plt.plot(NEW_N, NEW_NA, c='b')

plt.figure()
plt.title(f"Final point Max with original data_set: point={N[MAX][:-1].size}")
plt.scatter( NEW_N[MAX], NEW_NA[MAX], c=label)
plt.plot(n, amplitude_max, c='b')

plt.figure()
plt.title("Corespondance entre fréquence et amplitude rempaquable")
plt.plot(np.arange(len(X4)), X4)
plt.scatter(np.arange(len(X4)), X4, c=label)
plt.show()


"""///////////////////////////////////////////////"""
"""AffinityPropagation"""


print("")
print("AffinityPropagation")
cluster, label = fonction_clustering_AffinityPropagation(X)


#Affichage des données
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(X[:,0], X[:,1], X[:,2], c=label, marker='o', label="Data")
ax.scatter(cluster[:,0], cluster[:,1], cluster[:,2], c='r', marker='+', label="Cluster")

ax.set_xlabel('Différence des ordonnées')
ax.set_ylabel('Différence des abscisses')
ax.set_zlabel('Ordonnées')
ax.legend()
plt.show()


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(X[:,1], X[:,2], X[:,3], c=label, marker='o', label="Data")
ax.scatter(cluster[:,1], cluster[:,2], cluster[:,3], c='r', marker='+', label="Cluster")

ax.set_xlabel('Différence des ordonnées')
ax.set_ylabel('Différence des abscisses')
ax.set_zlabel('Ordonnées')
ax.legend()
plt.show()

print("\ncluster:\n",cluster)
print("\nlabel",label)

nb_label, size_nb = np.unique(label, return_counts=True)

print("")
print("nb_label",nb_label)
print("size_nb",size_nb)

print("")
# Afficher les éléments uniques et leur comptage
for element, compteur in zip(nb_label, size_nb):
    print(f"Élément {element} : {compteur} occurrences")


"""//////////////////////////"""

print("")
print("Affichage des données")

plt.figure()
plt.title(f"Final point with Max Final point: point={N[MAX][:-1].size}")
plt.scatter( NEW_N[MAX], NEW_NA[MAX], c=label)
plt.plot(NEW_N, NEW_NA, c='b')

plt.figure()
plt.title(f"Final point Max with original data_set: point={N[MAX][:-1].size}")
plt.scatter( NEW_N[MAX], NEW_NA[MAX], c=label)
plt.plot(n, amplitude_max, c='b')

plt.figure()
plt.title("Corespondance entre fréquence et amplitude rempaquable")
plt.plot(np.arange(len(X4)), X4)
plt.scatter(np.arange(len(X4)), X4, c=label)
plt.show()





"""///////////////////////////////////////////////"""
"""Spectral"""

print("")
print("Spectral")
label = fonction_clustering_Spectral(X, NEW_NA, MAX)


#Affichage des données
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(X[:,0], X[:,1], X[:,2], c=label, marker='o', label="Data")

ax.set_xlabel('Différence des ordonnées')
ax.set_ylabel('Différence des abscisses')
ax.set_zlabel('Ordonnées')
ax.legend()
plt.show()


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(X[:,1], X[:,2], X[:,3], c=label, marker='o', label="Data")

ax.set_xlabel('Différence des ordonnées')
ax.set_ylabel('Différence des abscisses')
ax.set_zlabel('Ordonnées')
ax.legend()
plt.show()


print("\ncluster:\n",cluster)
print("\nlabel",label)

nb_label, size_nb = np.unique(label, return_counts=True)

print("")
print("nb_label",nb_label)
print("size_nb",size_nb)

print("")
# Afficher les éléments uniques et leur comptage
for element, compteur in zip(nb_label, size_nb):
    print(f"Élément {element} : {compteur} occurrences")


"""//////////////////////////"""

print("")
print("Affichage des données")


plt.figure()
plt.title(f"Final point with Max Final point: point={N[MAX][:-1].size}")
plt.scatter( NEW_N[MAX], NEW_NA[MAX], c=label)
plt.plot(NEW_N, NEW_NA, c='b')

plt.figure()
plt.title(f"Final point Max with original data_set: point={N[MAX][:-1].size}")
plt.scatter( NEW_N[MAX], NEW_NA[MAX], c=label)
plt.plot(n, amplitude_max, c='b')

plt.figure()
plt.title("Corespondance entre fréquence et amplitude rempaquable")
plt.plot(np.arange(len(X4)), X4)
plt.scatter(np.arange(len(X4)), X4, c=label)
plt.show()


print("")
plt.figure()
plt.title("Affichage des différentes fréquences")
list = np.array([])

for i in range(NEW_N.size-1):
      
      a = Pxx[:100, NEW_N[i]]
      list = np.append(list, a)
      plt.plot(np.arange(a.size), a)

plt.show()

print("list.shape", list.shape)
list = list.reshape(-1, a.size)
print("list.shape", list.shape)
print("list",list)


list_max = np.max(list, axis=0)
plt.figure()
plt.title("Max des fréquences")
plt.plot(np.arange(list_max.size), list_max)
plt.show()


print("")
print("Pxx:",Pxx.shape,"\n",Pxx)

print("")
print("freqs:",frequencies.shape,"\n",frequencies)

print("")
print("bins:",times.shape,"\n",times)

#Boolean Indexing: Retire toute les valeurs dont la fréquence est supérieur à max_freq
spec_freqs=frequencies[(frequencies<1000)&(frequencies>0)]
nb=spec_freqs.shape[0]
spec_Pxx=Pxx[:nb,:]
spec_bins=times[:]

spec_bins, spec_freqs=np.meshgrid(spec_bins, spec_freqs)

print("")
print("spec_Pxx:",spec_Pxx.shape,"\n",spec_Pxx)

print("")
print("spec_freqs:",spec_freqs.shape,"\n",spec_freqs)

print("")
print("spec_bins:",spec_bins.shape,"\n",spec_bins)

"""
#Affichage des fréquence par le temps
n=np.arange(0, spec_Pxx.shape[1], 1)

for i in range(spec_Pxx.shape[0]):

    y_graph.append(spec_Pxx[i,:])
    x_graph.append(n)

fonction_graphque_comparaison(x_graph, y_graph, nom_graphique="Superposition des fréquences par le temps"
                              , x_legend="Time", y_legend="Amplitude", genre="all_plot")

fonction_animation(spec_Pxx, spec_freqs, True)

ax =plt.axes(projection='3d')
#ax.view_init(roll=90)
ax.plot_surface(spec_bins , spec_freqs,  spec_Pxx, cmap='Spectral')
ax.set_xlabel('Time [s]')
ax.set_ylabel('Fréquence en Hz')
ax.set_zlabel('Amplitude (dB/Hz)')
plt.title(f"Graphique 3D du fichier son: {fichier_audio_mono}")
plt.show()
"""