
import collections
from collections import Counter

#What is a containers, a container can be a list, a set, a dict, a tuple

#String
print("")
c = Counter("gallad") 
print(c)
print(list(c.elements()))
print(list(c.most_common(2)))

#List
print("")
c = Counter(["a", "b", "c", "z", "a"]) 
print(c)
print(list(c.elements()))
print(list(c.most_common(2)))

#Dict
print("")
c = Counter({"a":1, "b":2, "c":3}) 
print(c)
print(list(c.elements()))
print(list(c.most_common(2)))

#key_world
print("")
c = Counter(dog= 4, cat=2, fish=5, bird=1, cow=3) 
print(c)
print(c["cat"])
print(c["puppy"]) #Ne retourne pas d'erreur, juste 0 si le key_world n'exite pas
print(list(c.elements()))
print(list(c.most_common(2)))

#c.elements() affiche les élément du containers, auxquelle est associé a key_wold et a number

#c.most_common(2) affiche les élément les plus communs, le nombre d'élement montrer est définie par le nombre dans la paranthèse, ici 2.
#Si rien n'est rentré , la méthode retounrne les élément par odre décroissant de leus fréquences d'apparisons

#subtract
print("")
c = Counter(a=4, b=2, c=0, d=-2)
print("c",list(c.elements()))

e = Counter(a=1, b=2, c=1, d=1) 
print("e",list(e.elements()))
f = Counter(a=4, b=2, c=0, d=-2)
print("f",list(f.elements()))

d = ["a", "b", "c", "a"] 

c.subtract(d) 
print("res",c) 

f.subtract(e) 
print("res",f) 

#subtract soutrait les nombres associés au key_wold entre deux counter ou un counter et une list

#update
print("")
c = Counter(a=4, b=2, c=0, d=-2)
print("c",list(c.elements()))

e = Counter(a=1, b=2, c=1, d=1) 
print("e",list(e.elements()))
f = Counter(a=4, b=2, c=0, d=-2)
print("f",list(f.elements()))

d = ["a", "b", "c", "a"] 

c.update(d) 
print("res",c) 

f.update(e) 
print("res",f) 

#update addition les nombres associés au key_wold entre deux counter ou un counter et une list

#clear()
print("")
c = Counter(a=4, b=2, c=0, d=-2)
print("c",list(c.elements()))
c.clear()
print(c)

#clear() vide le counter

#Operation  two counters
print("")
e = Counter(a=1, b=2, c=1, d=1) 
print("e",list(e.elements()))
f = Counter(a=4, b=2, c=0, d=-2)
print("f",list(f.elements()))

print(e+f) #add two counters
print(e-f) #sub two counters
print(e&f) #intersection two 
print(e|f) #union two counters