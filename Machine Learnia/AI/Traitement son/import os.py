import os
from mutagen.mp4 import MP4
import shutil

# Chemin vers le dossier contenant les fichiers audio m4a
dossier_source = "Desktop\Document\Musique (m4a) - Copie"

# Chemin vers le dossier de destination (où seront créés les sous-dossiers)
dossier_destination = "Desktop\Document\Musique (m4a) - Copie"

# Parcourir les fichiers dans le dossier source
for fichier in os.listdir(dossier_source):
    if fichier.endswith(".m4a"):
        chemin_fichier = os.path.join(dossier_source, fichier)

        # Récupérer les informations de l'artiste à partir des tags MP4
        audio = MP4(chemin_fichier)
        artiste = audio.get("\xa9ART", ["Inconnu"])[0]

        # Créer le chemin vers le sous-dossier
        chemin_sous_dossier = os.path.join(dossier_destination, artiste)

        # Vérifier si le sous-dossier existe, sinon le créer
        if not os.path.exists(chemin_sous_dossier):
            os.makedirs(chemin_sous_dossier)

        # Déplacer le fichier audio dans le sous-dossier
        shutil.move(chemin_fichier, chemin_sous_dossier)

        for sous_fichier in os.listdir(chemin_sous_dossier):
            if sous_fichier.endswith(".m4a"):
                sous_chemin_fichier = os.path.join(chemin_sous_dossier, sous_fichier)

                # Récupérer les informations de l'artiste à partir des tags MP4
                audio = MP4(sous_chemin_fichier)
                artiste = audio.get("\xa9alb", ["Inconnu"])[0]

                # Créer le chemin vers le sous-dossier
                chemin_sous_sous_dossier = os.path.join(dossier_destination, artiste)

                # Vérifier si le sous-dossier existe, sinon le créer
                if not os.path.exists(chemin_sous_sous_dossier):
                    os.makedirs(chemin_sous_sous_dossier)

                # Déplacer le fichier audio dans le sous-dossier
                shutil.move(sous_chemin_fichier, chemin_sous_sous_dossier)
