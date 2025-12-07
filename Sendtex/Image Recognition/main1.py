
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)


i = Image.open('images/dot.png')
iar = np.asarray(i)

print (iar)

plt.figure()
plt.imshow(iar)
plt.show()