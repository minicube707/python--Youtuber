import numpy as np

#Broadcasting
print("#Broadcasting")
print("")

print("Pour faire la somme la somme de deux Matrice, il suffit de faire; C=A+B")

A=np.array([[1,2,3],
            [4,5,6]])

B=np.array([[4,5,6],
            [7,8,9]])
C=A+B

print("")
print("A=")
print(A)

print("")
print("B=")
print(B)

print("")
print("C=")
print(C)

print("")
print("Pour faire du Broadcasting, il faut que les Matrices est les même dimension")
print("A est de dimension ",A.shape)
print("B est de dimension ",B.shape)
print("Est donne une Matrice de même dimension",C.shape)

print("")
print("Sauf dans certains cas")
print("D=A+2")
D=A+2

print("")
print("D=")
print(D)

print("")
print("Ici, '2' est une Matrice de dimension (1,1), que l'on a étiré pour qu'elle fasse les dimension de A")

print("")
print("Autre exemple")

E=np.array([[1],
            [2]])

print("")
print("E=")
print(E)

print("")
print("F=A+E")
F=A+E

print("")
print("F=")
print(F)

print("")
print("Ici, 'E' est une Matrice de dimension,",E.shape," que l'on a étiré pour qu'elle fasse les dimension de A, soit",A.shape)

print("")
print("Autre exemple")
G=np.array([[1,2,3,4]])

print("")
print("G=")
print(G)

H=np.array([[1],
            [2],
            [3]
            ,[4]])

print("")
print("H=")
print(H)
print("")

print("I=H+G")
I=H+G
print("I=")
print(I)
print("")
print("Ici, 'H' et 'G' on était étiré pour qu'elle puisse avoir les dimension de l'autre")

print("")
print("Derneir exemple")
print("H=")
print(H)
print("Les dimension de H sont ",H.shape)

print("")
J=np.ones(4,)
print("J=")
print(J)
print("Les dimension de J sont ",J.shape)

print("")
K=H+J
print("K=H+J")
print("K=")
print(K)

print("")
print("Ici l'opération peut se faire car le '4' est considérer comme le dernier élément, donc affilié à l'axe 1")
print("C'est pourquoi, il faut toujours redimensionner ses Matrices")

print("")
print("Alors que si je fais J=J.reshape(4,1)")

J=J.reshape(4,1)

print("")
print("J=")
print(J)
print("Les dimension de J sont ",J.shape)

K=H+J

print("")
print("K=H+J")
print("K=")
print(K)

print("Le '4' est considéré comme le premier élément donc affilié à l'axe 0 et\n le '1' est considéré comme le dernier élément donc affilié à l'axe 1")
