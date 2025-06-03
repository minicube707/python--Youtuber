
li = [1, 2, 3, 4, 5, 6, 7, 8, 9]

#Classique function
def  func(x):
    return x*2

a = func(4)
print(a)

#Function lambda
func2 = lambda x : x*3
print(func2(4))

isodd = lambda x : x%2 == 1
print(list(map(isodd, li)))

isodd = lambda x : x%2 == 1
print(list(filter(isodd, li)))

#Multiple parameter
func3 = lambda x,y : x+y
print(func3(6, 5))

#Default parameter
func3 = lambda x,y=1 : x+y
print(func3(6))

