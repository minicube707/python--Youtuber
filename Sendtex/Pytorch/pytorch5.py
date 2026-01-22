import os
import cv2
import numpy as np
from tqdm import tqdm
import torch
import matplotlib.pyplot as plt

#Link to the dataset Cat vs Dog
#https://www.microsoft.com/en-us/download/details.aspx?id=54765

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)

REBUILD_DATA = False

#Cette ligne s’exécute IMMÉDIATEMENT, pas quand tu crées l’objet.
#👉 En Python :
# - le corps d’une classe est exécuté au moment où la classe est définie
# - pas quand DogsVSCats() est appelé

class DogsVSCats():
    IMZ_SIZE = 50

    CATS = "PetImages/Cat"
    DOGS = "PetImages/Dog"
    LABELS = {CATS: 0, DOGS: 1}

    training_data = []
    catcount = 0
    dogcount = 0


    def make_training_data(self):

        os.chdir("kagglecatsanddogs_5340")

        for label in self.LABELS:
            print(label)
            for f in tqdm(os.listdir(label)):
                try:
                    path = os.path.join(label, f)
                    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    img = cv2.resize(img, (self.IMZ_SIZE, self.IMZ_SIZE))
                    self.training_data.append([np.array(img), np.eye(2)[self.LABELS[label]]])

                    if label == self.CATS:
                        self.catcount += 1
                    else:
                        self.dogcount += 1
                
                except Exception as e:
                    pass
                    print(str(e))

        os.chdir("..")

        np.random.shuffle(self.training_data)
        np.save("training_data.npy", np.array(self.training_data, dtype=object))
        
        print('Cats:', self.catcount)
        print('Dogs:', self.dogcount)

if REBUILD_DATA:
    dogsvcats = DogsVSCats()
    dogsvcats.make_training_data()


else:

    training_data = np.load("training_data.npy", allow_pickle=True)
    print(len(training_data))

    X = torch.Tensor([i[0] for i in training_data]).view(-1,50,50)
    X = X/255.0
    y = torch.Tensor([i[1] for i in training_data])

    plt.figure()
    plt.imshow(X[0], cmap="gray")
    plt.show()

    print(y[0])
