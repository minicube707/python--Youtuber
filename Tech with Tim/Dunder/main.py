#Dunder/Magic Methods in Python


#"Dunder" means "Double UNDERscore"
#These are special methods surrounded by double underscores.
#Examples: __init__, __str__, __add__, __len__, etc.

str1 = "hello"
str2 = "world"

def func():
    pass


#In Python, EVERYTHING is an object.
#Even a function is an instance of a class.
print(type(func))
#-> <class 'function'>
#This means "func" is an object of type "function".

#------------------------------
#Example 1: String addition
#------------------------------

#This syntax:
print(str1 + str2)

#Is actually shorthand for:
print(str1.__add__(str2))

#The + operator automatically calls the magic method __add__()
#So:
#str1 + str2  ==  str1.__add__(str2)

#This syntax:
print(len(str1))

#Is actually shorthand for:
print(str1.__len__())
#The len() function automatically calls the magic method __len__()
#So:
#len(str1)  ==  str1.__len__()