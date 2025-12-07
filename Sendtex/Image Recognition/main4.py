
from PIL import Image
import numpy as np
from collections import Counter
import os

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)

def whatNumIsThis(filePath):

    matchedAr = []
    loadExamps = open('numArEx.txt','r').read()
    loadExamps = loadExamps.split('\n')

    i = Image.open(filePath)
    iar = np.array(i)
    iarl = iar.tolist()

    inQuestion = str(iarl)

    for eachExample in loadExamps:
        try:
            splitEx = eachExample.split('::')
            currentNum = splitEx[0]
            currentAr = splitEx[1]
            
            eachPixEx = currentAr.split('],')
            eachPixInQ = inQuestion.split('],')

            x = 0

            while x < len(eachPixEx):
                #If the pixel match with the database, add the number to a list
                if eachPixEx[x] == eachPixInQ[x]:
                    matchedAr.append(int(currentNum))

                x+=1
        except Exception as e:
            print(str(e))
                
    print(matchedAr)
    x = Counter(matchedAr)
    print(x)
    print(x[0])

whatNumIsThis('images/test1.png')
whatNumIsThis('images/test2.png')