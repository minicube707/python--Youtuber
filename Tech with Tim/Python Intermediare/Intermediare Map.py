
li = [1, 2, 3, 4,5 , 6, 7, 8, 9, 10]

def func(x):
    return x**x

#Test 1
print("Test 1")
print(list(map(func, li)))
print([func(x) for x in li])
print("")

#Test2
print("#Test2")
print([func(x) for x in li if x%2 == 0])