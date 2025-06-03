import matplotlib.pyplot as plt
import numpy as np
import os 

from scipy.signal import argrelextrema 
from scipy.io import wavfile
from scipy.io.wavfile import write

from sklearn. preprocessing import StandardScaler
from Def_spectrographe import  func_cut
from Def_graphique import fonction_graphique, fonction_graphque_comparaison
from Def_animation import fonction_animation
from Def_preprocessing import function_vecteur, batage
from Def_clustering import fonction_clustering

import warnings

def find_indice(matrice, val, axis, indice):

      find = False
      i=0

      if axis == 0:
            while (find == False) and (i < Pxx.shape[0]):
                  if matrice[i,indice] == val:
                        find=True
                  else:
                        i+=1

      elif axis == 1:
            while (find == False) and (i < Pxx.shape[1]):
                  if matrice[indice,i] == val:
                        find=True
                  else:
                        i+=1
      else:
            raise ValueError("axis doit être compris entre 0 et 1")
      return i
      

# Ignorer les UserWarnings
warnings.filterwarnings("ignore", category=UserWarning)

#Dossier actuel
current_directory = os.getcwd()
print("Vous êtes actuellement dans le dossier :", current_directory)

if current_directory == "C:\\Users\\flore\\Desktop\\Document\\Programme\\Python\\AI\\Traitement son" :
      os.chdir("..\..\..\..\..\..")

      current_directory = os.getcwd()
      print("Vous êtes actuellement dans le dossier :", current_directory)


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

plt.figure()
plt.plot(np.arange(audio_data.shape[0]), audio_data[:, 0], label='Canal Gauche')
plt.plot(np.arange(audio_data.shape[0]), audio_data[:, 1], label='Canal Droit')
plt.xlabel('Échantillons')
plt.ylabel('Amplitude')
plt.title('Signal Audio - Canaux Gauche et Droit')
plt.legend()
plt.show()

print("")
print(f"number of channels of stereo= {audio_data.shape[1]}")
#number of channels = 2

length = audio_data.shape[0] / sample_rate
print("")
print(f"length = {length}s")


#Tracez la forme d’onde.
time = np.linspace(0., length, audio_data.shape[0])

x_graph=[time,time]
y_graph=[audio_data[:,0], audio_data[:,1]]
label=[ "Left channel", "Right channel"]
alpha=[0.7, 0.7]

fonction_graphque_comparaison( x_graph, y_graph, f'Analyse de fichier: {fichier_audio}', genre="all_plot", x_legend="Time [s]"
                              , y_legend="Amplitude", label_graph=label, alpha_graph=alpha)


# Convertir les échantillons en valeurs d'amplitude réelle
amplitude = np.abs(audio_data)


# Calculer l'amplitude en dB
amplitude_db = 20 * np.log10(amplitude)


#Tracez la forme d’onde en db.
x_graph=[time,time]
y_graph=[amplitude_db[:,0],  amplitude_db[:,1]]
label=[ "Left channel", "Right channel"]
alpha=[0.7, 0.7]

fonction_graphque_comparaison( x_graph, y_graph, f'Analyse de fichier: {fichier_audio}', x_legend="Time [s]"
                              , y_legend="Amplitude", genre=['plot', 'plot'], label_graph=label, alpha_graph=alpha)


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


#Fs : La fréquence d'échantillonnage du signal en Hz (Hertz).
#Elle spécifie combien d'échantillons par seconde sont pris pour enregistrer le signal.
#Par exemple, si votre signal est échantillonné à 44100 Hz, vous définiriez Fs sur 44100.

#NFFT: La longueur de la fenêtre de transformation de Fourier à court terme (STFT).
#Cela détermine la résolution fréquentielle du spectrogramme.
#Une valeur plus grande de NFFT donne une meilleure résolution en fréquence mais une moins bonne résolution en temps.

#noverlap : Le nombre de points de chevauchement entre les fenêtres successives de la STFT.
#Cela contrôle la lissage temporel dans le spectrogramme. Une valeur plus élevée de noverlap donne une lissage temporel plus important.

#xextent : Les limites des axes x (temps) pour le spectrogramme.
#Vous pouvez les utiliser pour zoomer ou afficher une sous-section du spectrogramme complet.
#Ici, je veux le spectrographe de la seconde 0 à la seconde 3


NFFT = 2048
noverlap = 2000
Fs = sample_rate_mono

"""
fig, ax2 = plt.subplots()
Pxx, freqs, bins, im = ax2.specgram(audio_data_mono, NFFT=NFFT, Fs=Fs, noverlap=noverlap)
# The `specgram` method returns 4 objects. They are:
# - Pxx: the periodogram
# - freqs: the frequency vector
# - bins: the centers of the time bins
# - im: the .image.AxesImage instance representing the data in the plot
plt.show()
"""

Pxx, freqs, bins=func_cut(audio_data=audio_data_mono ,sample_rate=sample_rate_mono ,NFFT=NFFT, Fs=Fs, noverlap=noverlap)


#Pxx (le periodogramme) : Le periodogramme est une estimation de la densité spectrale de puissance (PSD) (Power Spectral Density) du signal audio.
#Cela signifie qu'il indique la répartition de la puissance du signal dans différentes fréquences.
#Le periodogramme est calculé à partir de la transformée de Fourier à court terme (STFT) du signal.
#En d'autres termes, Pxx contient l'amplitude spectrale à chaque fréquence pour chaque intervalle de temps. 
#C'est une matrice où les lignes représentent les fréquences et les colonnes représentent les tranches de temps.

#freqs (le vecteur de fréquence) : C'est un tableau NumPy qui contient les valeurs de fréquence correspondant aux lignes de la matrice Pxx.
#Chaque élément de freqs correspond à la fréquence du signal à une position donnée dans Pxx.

#bins (les centres des tranches de temps) : C'est un tableau NumPy qui contient les valeurs temporelles correspondant aux colonnes de la matrice Pxx.
#Chaque élément de bins représente le centre temporel d'une tranche de temps dans laquelle l'analyse spectrale a été effectuée

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
m = np.arange(0, frequence_max.size, 1)



max_indices = np.argmax(Pxx, axis=0)
coord_max = np.unravel_index(max_indices, Pxx.shape)    # Obtenir les coordonnées (ligne, colonne) de ces maxima
coord_max = coord_max[1]
print("\ncoord_max",coord_max)                          # coord_max est un tuple de tableaux, chaque tableau contenant les coordonnées correspondant à une colonne


indices_max_amplitudes = np.argmax(Pxx, axis=0) # Indices des fréquences correspondant aux amplitudes maximales
frequences_max_amplitudes = freqs[indices_max_amplitudes]   # Fréquences correspondant aux amplitudes maximales

print("\nfrequences_max_amplitudes.shape",frequences_max_amplitudes.shape) 
print("frequences_max_amplitudes",frequences_max_amplitudes)          # Affichage des fréquences correspondant aux amplitudes maximales

stand_scaler = StandardScaler()
freq_graph = stand_scaler.fit_transform(frequences_max_amplitudes.reshape(-1, 1))

stand_scaler = StandardScaler()
ampl_graph = stand_scaler.fit_transform(amplitude_max.reshape(-1, 1))

stand_scaler = StandardScaler()
coord_max_graph = stand_scaler.fit_transform(coord_max.reshape(-1, 1))

fonction_graphique(np.arange(coord_max.size), coord_max, "coord_max", "plot")
fonction_graphique(np.arange(frequences_max_amplitudes.size), frequences_max_amplitudes, "freq max amp", "plot")


fonction_graphque_comparaison([np.arange(freq_graph.size), np.arange(ampl_graph.size), np.arange(coord_max_graph.size)], [freq_graph, ampl_graph, coord_max_graph], nom_graphique="graph", genre="all_plot", label_graph=["fre", "ampl", "coor"])

print("\ncoord_max.shape",coord_max.shape)
print("coord_max.size",coord_max.size)
print("coord_max",coord_max)




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
print("Liste des indices minima locaux")
print(minima_indices)
print("\nListe des  minima locaux")
print(amplitude_max[minima_indices])


# Trouvez les indices des maximums locaux
maxima_indices = argrelextrema(amplitude_max, np.greater)
maxima_indices = list(maxima_indices)
maxima_indices = maxima_indices[0]

print("\nmaxima_indices.shape", maxima_indices.shape)
print("maxima_indices.size", maxima_indices.size)
print("Liste des indices maxima  locaux")
print(maxima_indices)
print("\nListe des maxima locaux")
print(amplitude_max[maxima_indices])

                                   
#Boolean indexing pour retirer les valeurs <1
new_inidice_maxima = n[maxima_indices][amplitude_max[maxima_indices]>1]
new_inidice_minima = n[minima_indices][amplitude_max[minima_indices]>1]


#Ajout du 0 étant que dernière valeur minimal retiré
first_indice_minima=n[minima_indices][amplitude_max[minima_indices]<1][-1:]
new_inidice_minima = np.insert(new_inidice_minima, 0, first_indice_minima)

print("\nnew_inidice_maxima.shape",new_inidice_maxima.shape)
print("new_inidice_maxima.size", new_inidice_maxima.size)
print("new_inidice_maxima\n", new_inidice_maxima)

print("\nnew_inidice_minima.shape",new_inidice_minima.shape)
print("new_inidice_minima.size", new_inidice_minima.size)
print("new_inidice_minima\n", new_inidice_minima)


print("\namplitude_max[new_inidice_maxima].shape", amplitude_max[new_inidice_maxima].shape)
print("amplitude_max[new_inidice_maxima].size", amplitude_max[new_inidice_maxima].size)
print("amplitude_max[new_inidice_maxima]\n", amplitude_max[new_inidice_maxima])

print("\nn.shape[new_inidice_maxima]", n[new_inidice_maxima].shape)
print("n.size[new_inidice_maxima]", n[new_inidice_maxima].size)
print("n[new_inidice_maxima]\n", n[new_inidice_maxima])


new_n, new_amplitude_max, masque = function_vecteur(new_inidice_minima, new_inidice_maxima, n, amplitude_max, 0.15)

new_coord_max = coord_max[batage(new_inidice_minima, new_inidice_maxima)]
new_amplitude_max = np.append(new_amplitude_max, 0)
new_n = np.append(new_n, len(n))

print("\nmasque.shape",masque.shape)
print("masque.size",masque.size)
print("masque",masque)

print("\nnew_coord_max.shape",new_coord_max.shape)
print("new_coord_max.size",new_coord_max.size)
print("new_coord_max",new_coord_max)

print("\nnew_coord_max[masque].shape",new_coord_max[masque].shape)
print("new_coord_max[masque].size",new_coord_max[masque].size)
print("new_coord_max[masque]",new_coord_max[masque])

print("\nnew_n.shape",new_n.shape)
print("new_n.size",new_n.size)
print("new_n",new_n)

print("\nnew_amplitude_max.shape",new_amplitude_max.shape)
print("new_amplitude_max.size",new_amplitude_max.size)
print("new_amplitude_max",new_amplitude_max)

fonction_graphique(new_n[:-1], new_coord_max[masque], "", "plot")
#Affichage des données vu par l'ordinateur
"""
plt.figure()
plt.title(f"Point de base: point={new_inidice_maxima.size + new_inidice_minima.size}")
plt.scatter(n[new_inidice_maxima], amplitude_max[new_inidice_maxima], c='b')
plt.scatter(n[new_inidice_minima], amplitude_max[new_inidice_minima], c='r')
plt.plot(n, amplitude_max)

plt.figure()
plt.title(f"New point de base: point={new_n.size}")
plt.scatter( new_n, new_amplitude_max)
plt.plot(n, amplitude_max, c='b')
plt.plot(new_n, new_amplitude_max, c='r')

plt.figure()
plt.title(f"New point de base: point={new_n.size}")
plt.scatter( new_n, new_amplitude_max)
plt.plot(n, amplitude_max, c='r')

plt.figure()
plt.title(f"New point de base: point={new_n.size}")
plt.scatter( new_n, new_amplitude_max)
plt.plot(new_n, new_amplitude_max, c='b')
plt.show()
"""
new_maxima_indices = np.array(argrelextrema(new_amplitude_max, np.greater))
new_minima_indices = np.array(argrelextrema(new_amplitude_max, np.less))

new_maxima_indices = new_maxima_indices[0]
new_minima_indices = new_minima_indices[0]

if new_minima_indices.size < new_maxima_indices.size:
        new_minima_indices = np.insert(new_minima_indices, 0, 0)


#Indice
print("\nnew_maxima_indices.shape",new_maxima_indices.shape)
print("new_maxima_indices.size",new_maxima_indices.size)
print("new_maxima_indices",new_maxima_indices)

print("\nnew_minima_indices.shape",new_minima_indices.shape)
print("new_minima_indices.size",new_minima_indices.size)
print("new_minima_indices",new_minima_indices)


#X
print("\nnew_n[new_maxima_indices].shape",new_n[new_maxima_indices].shape)
print("new_n[new_maxima_indices].size",new_n[new_maxima_indices].size)
print("new_n[new_maxima_indices]",new_n[new_maxima_indices])

print("\nnew_n[new_minima_indices].shape",new_n[new_minima_indices].shape)
print("new_n[new_minima_indices].size",new_n[new_minima_indices].size)
print("new_n[new_minima_indices]",new_n[new_minima_indices])


#Y
print("\nnew_amplitude_max[new_maxima_indices].shape",new_amplitude_max[new_maxima_indices].shape)
print("new_amplitude_max[new_maxima_indices].size",new_amplitude_max[new_maxima_indices].size)
print("new_amplitude_max[new_maxima_indices]",new_amplitude_max[new_maxima_indices])

print("\nnew_amplitude_max[new_minima_indices].shape",new_amplitude_max[new_minima_indices].shape)
print("new_amplitude_max[new_minima_indices].size",new_amplitude_max[new_minima_indices].size)
print("new_amplitude_max[new_minima_indices]",new_amplitude_max[new_minima_indices])

new_n2 = batage(new_n[new_minima_indices], new_n[new_maxima_indices])
new_amplitude_max2 = batage(new_amplitude_max[new_minima_indices], new_amplitude_max[new_maxima_indices])

new_amplitude_max2 = np.append(new_amplitude_max2, 0)
new_n2 = np.append(new_n2, len(n))

print("\nnew_n2.shape",new_n2.shape)
print("new_n2.size",new_n2.size)
print("new_n2",new_n2)

print("\nnew_amplitude_max2.shape",new_amplitude_max2.shape)
print("new_amplitude_max2.size",new_amplitude_max2.size)
print("new_amplitude_max2",new_amplitude_max2)

#Affichage des données vu par l'ordinateur
plt.figure()
plt.title(f"Nombre de point: {new_n2.size}")
plt.scatter(new_n2, new_amplitude_max2)

plt.figure()
plt.title(f"Nombre de point: {n[new_inidice_maxima].size + n[new_inidice_minima].size}")
plt.scatter(n[new_inidice_maxima], amplitude_max[new_inidice_maxima], c='b')
plt.scatter(n[new_inidice_minima], amplitude_max[new_inidice_minima], c='r')

plt.figure()
plt.title(f"Nombre de point: {n.size}")
plt.scatter(n, amplitude_max)
plt.show()


#Affichage des repères max
tab3_max=[]
tab4_max=[]
tab5_max=[]
tab6_max=[]

for i in range(len(new_n[new_maxima_indices])-1):
      tab3_max.append(new_n[new_maxima_indices][i+1] - new_n[new_maxima_indices][i])
      tab4_max.append(new_amplitude_max[new_maxima_indices][i+1] - new_amplitude_max[new_maxima_indices][i])
      tab5_max.append(new_amplitude_max[new_maxima_indices][i])
      d = find_indice(Pxx, new_amplitude_max[new_maxima_indices][i], 0, new_n[new_maxima_indices][i])
      tab6_max.append(d)

print("\ntab3.shape",len(tab3_max))
print("tab3",tab3_max)
print("\ntab4.shape",len(tab4_max))
print("ntab4",tab4_max)
print("\ntab5.shape",len(tab5_max))
print("tab5",tab5_max)
print("\ntab6.shape",len(tab6_max))
print("tab5",tab6_max)


X  = np.column_stack((tab3_max, tab4_max, tab5_max, tab6_max))
print("\nX",X)

stand_scaler = StandardScaler()
X = stand_scaler.fit_transform(X)

print("\nX",X)

cluster, label = fonction_clustering(X, 10)


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

ax.scatter(X[:,0], X[:,1], X[:,3], c=label, marker='o', label="Data")
ax.scatter(cluster[:,0], cluster[:,1], cluster[:,3], c='r', marker='+', label="Cluster")

ax.set_xlabel('Différence des ordonnées')
ax.set_ylabel('Différence des abscisses')
ax.set_zlabel('Ordonnées')
ax.legend()
plt.show()


print("\ncluster:\n",cluster)
print("\nlabel",label)

X_cluster=cluster[:,0]
Y_cluster=cluster[:,1]

plt.figure()
plt.title(f"New point Max with original data_set: point={new_n[new_maxima_indices][:-1].size}")
plt.scatter( new_n[new_maxima_indices][:-1], new_amplitude_max[new_maxima_indices][:-1], c=label)
plt.plot(n, amplitude_max, c='b')

plt.figure()
plt.title(f"New point Max with original data_set: point={new_n[new_maxima_indices][:-1].size}")
plt.scatter( new_n[new_maxima_indices][:-1], new_amplitude_max[new_maxima_indices][:-1], c=label)
plt.plot(new_n2, new_amplitude_max2, c='b')

plt.figure()
plt.title(f"New point Max with original data_set: point={new_n[new_maxima_indices][:-1].size}")
plt.scatter( new_n[new_maxima_indices][:-1], new_amplitude_max[new_maxima_indices][:-1], c=label)
plt.show()






""""

list_n = []
unique_elements, counts = np.unique(label, return_counts=True)
print("Les élément unique ", unique_elements)

for i in range(np.max(unique_elements)+1):
      elemnt = new_n[new_maxima_indices][:-1][label==i]
      print("elelemt", elemnt)
      list_n.append(elemnt)
print("lst n", list_n)


list_f2 = []
for i  in range(len(list_n)):
      a = list_n[i]
      list_f3 = []
      for k in range(len(a)):
            b = a[k]
            list_f = []
            for j in range(len(new_n2)):
                  if b == new_n2[j]:
                        list_f.append(new_n2[j-1])
                        list_f.append(new_n2[j+1])
            list_f3.append(list_f)
      list_f2.append(list_f3)
print("listedfgtrf", list_f2)

main_list = []
for i in range(len(list_f2)):
      a = list_f2[i]
      list_main2= []
      for j in range(len(a)):
            b = a[j]
            list_main1 = Pxx[:,b[0]:b[1]+1]
            list_main2.append(list_main1)
      main_list.append(list_main2)

print("len(list_main)",len(main_list))


# Normalisez le signal à la plage [-1, 1]
a =main_list[0]
b =a[0]
print("b: ",b)


audio_signal = np.fft.irfft(np.sqrt(Pxx))
print("audio_signal.shape", audio_signal.shape)

# Étape 2 : Normalisation
audio_signal  = np.int16(audio_signal / np.max(np.abs(audio_signal)) * 32767)

# Écrivez le signal audio dans un fichier WAV
write("signal_audio.wav", sample_rate_mono, audio_signal.astype(np.int32))
"""


#Affichage des repères min
tab3_min=[]
tab4_min=[]
tab5_min=[]
tab6_min=[]

for i in range(len(new_n[new_minima_indices])-1):
      tab3_min.append(new_n[new_minima_indices][i+1] - new_n[new_minima_indices][i])
      tab4_min.append(new_amplitude_max[new_minima_indices][i+1] - new_amplitude_max[new_minima_indices][i])
      tab5_min.append(new_amplitude_max[new_maxima_indices][i])
      e=find_indice(Pxx, new_amplitude_max[new_minima_indices][i], 0, new_n[new_minima_indices][i])
      tab6_min.append(e)

print("\ntab3",tab3_min)
print("\ntab4",tab4_min)
print("\ntab5",tab5_min)
print("\ntab6",tab6_min)

X  = np.column_stack((tab3_min, tab4_min, tab5_min, tab6_min))
print("\nX",X)

stand_scaler = StandardScaler()
X = stand_scaler.fit_transform(X)

print("\nX",X)

cluster, label = fonction_clustering(X, 10)


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

ax.scatter(X[:,0], X[:,1], X[:,3], c=label, marker='o', label="Data")
ax.scatter(cluster[:,0], cluster[:,1], cluster[:,3], c='r', marker='+', label="Cluster")

ax.set_xlabel('Différence des ordonnées')
ax.set_ylabel('Différence des abscisses')
ax.set_zlabel('Ordonnées')
ax.legend()
plt.show()

print("\ncluster:\n",cluster)
print("\nlabel",label)

X_cluster=cluster[:,0]
Y_cluster=cluster[:,1]


plt.figure()
plt.title(f"New point Min with original data_set: point={new_n[new_minima_indices][:-1].size}")
plt.scatter( new_n[new_minima_indices][:-1], new_amplitude_max[new_minima_indices][:-1], c=label)
plt.plot(n, amplitude_max, c='b')

plt.figure()
plt.title(f"New point Min with original data_set: point={new_n[new_minima_indices][:-1].size}")
plt.scatter( new_n[new_minima_indices][:-1], new_amplitude_max[new_minima_indices][:-1], c=label)
plt.plot(new_n2, new_amplitude_max2, c='b')

plt.figure()
plt.title(f"New point Min with original data_set: point={new_n[new_minima_indices][:-1].size}")
plt.scatter( new_n[new_minima_indices][:-1], new_amplitude_max[new_minima_indices[:-1]], c=label)
plt.show()

print("")
plt.figure()
list = np.array([])
for i in range(new_n2.size-1):
      a = Pxx[:100,new_n2[i]]
      list = np.append(list, a)
      plt.plot(np.arange(a.size), a)
plt.show()

print("list.shape", list.shape)
list = list.reshape(-1, a.size)
print("list.shape", list.shape)
print("list",list)

list_max = np.max(list, axis=0)
plt.figure()
plt.plot(np.arange(list_max.size), list_max)
plt.show()

list_max_axis_1 = np.max(list, axis=1)
plt.figure()
plt.plot(np.arange(list_max_axis_1.size), list_max_axis_1)
plt.show()


plt.figure()
list_a = np.array([])
list_b = np.array([])
for i in range(new_n2.size-1):
      a = Pxx[:100,new_n2[i]]

      maxima_indices = argrelextrema(a, np.greater)
      plt.scatter(maxima_indices, a[maxima_indices], c="r")

      minima_indices = argrelextrema(a, np.less)
      plt.scatter(minima_indices, a[minima_indices], c="b")

plt.plot(np.arange(list_max.size), list_max)
plt.show()


fonction_graphique(m, frequence_max, x_legend="Frequence", y_legend="Amplitude", nom_graphique="Graphique des plus hautes fréquences en fonction du temps", genre='plot')
fonction_graphique(m, frequence_var, x_legend="Frequence", y_legend="Variance de la Fréquence", nom_graphique="Graphique de la variance des fréquence en fonction du temps", genre='plot')
   
print("")
print("Pxx:",Pxx.shape,"\n",Pxx)

print("")
print("freqs:",freqs.shape,"\n",freqs)

print("")
print("bins:",bins.shape,"\n",bins)

#Boolean Indexing: Retire toute les valeurs dont la fréquence est supérieur à max_freq
spec_freqs=freqs[(freqs<1000)&(freqs>0)]
nb=spec_freqs.shape[0]
spec_Pxx=Pxx[:nb,:]
spec_bins=bins[:]

spec_bins, spec_freqs=np.meshgrid(spec_bins, spec_freqs)

print("")
print("spec_Pxx:",spec_Pxx.shape,"\n",spec_Pxx)

print("")
print("spec_freqs:",spec_freqs.shape,"\n",spec_freqs)

print("")
print("spec_bins:",spec_bins.shape,"\n",spec_bins)


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
