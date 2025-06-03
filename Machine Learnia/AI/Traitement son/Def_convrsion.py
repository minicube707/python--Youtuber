import os
from pydub import AudioSegment

def fonction_conversion_aac_to_wav(nom_dossier=None,nom_fichier=None):

    if nom_dossier==None:
        raise ValueError("Nom de dossier non renseignié")
    if nom_fichier==None:
        raise ValueError("Nom du fichier non renseignié")


    #Répertoire actuel
    current_directory = os.getcwd()
    print("\nRépertoire de travail actuel :", current_directory)


    #Déplacement dans l'ordi
    os.chdir(f"Desktop\Document\Musique\{nom_dossier}")


    #Répertoire actuel
    current_directory = os.getcwd()
    print("\nRépertoire de travail actuel :", current_directory)


    # Spécifiez le chemin du fichier .aac d'entrée et .wav de sortie
    fichier_aac = f"{nom_fichier}.acc"
    fichier_wav = f"{nom_fichier}.wav"


    # Chargez le fichier .aac en utilisant AudioSegment
    audio = AudioSegment.from_file(fichier_aac, format="aac")


    # Convertissez le fichier .aac en .wav
    audio.export(fichier_wav, format="wav")
    print("")
    print(f"Conversion terminée : {fichier_aac} -> {fichier_wav}")



    #Déplacement dans l'ordi
    os.chdir("..\..\..\..")


    #Répertoire actuel
    current_directory = os.getcwd()
    print("\nRépertoire de travail actuel :", current_directory)


def fonction_conversion_stereo_to_mono(fichier_audio):

    
    # Charger le fichier audio stéréo
    audio_stereo = AudioSegment.from_wav(fichier_audio)

    # Convertir en mono en prenant la moyenne des canaux gauche et droit
    audio_mono = audio_stereo.set_channels(1)
    fichier_mono=f"{fichier_audio}_mono.wav"

    # Exporter le fichier audio mono au format WAV
    audio_mono.export(fichier_mono, format="wav")
