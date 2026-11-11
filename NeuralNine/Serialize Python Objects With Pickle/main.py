
import pickle

# ============================================================
# Serialization in Python
#
# Serialization is the process of converting an object or 
# a data structure into a format that can be stored in a
# file or transmitted over a network. 
# In Python, the pickle module allows us to serialize 
# almost any Python object, including variables, lists, 
# dictionaries, and custom classes. 
# The pickle.dump() function is used to save an object, 
# while pickle.load() restores it to its original form. 
# This process is also called deserialization. 
# Serialization is particularly useful when we want to 
# save the state of a program and retrieve it later 
# without having to recreate all the objects manually.
# ============================================================


# ============================================================
# 1. WRITE AND READ BASIC DATA USING A TEXT FILE
# ============================================================

mytext = "Hello World"
myint = 42
myfloat = 3.1415926

filename = "mydata.txt"

# Write data
with open(filename, "w") as file:
    file.write(f"{mytext}\n")
    file.write(f"{myint}\n")
    file.write(f"{myfloat}\n")

# Read data
with open(filename, "r") as file:
    data = file.read().splitlines()

# Convert data to their original types
mytext = data[0]
myint = int(data[1])
myfloat = float(data[2])

print("TEXT FILE:")
print(f"{mytext=}")
print(f"{myint=}")
print(f"{myfloat=}")


# ============================================================
# 2. DICTIONARY
# ============================================================

mydict = {
    "A": 42,
    "B": 37,
    "H": 12
}

print("\nDICTIONARY:")
print(mydict)


# ============================================================
# 3. DEFINE A PERSON CLASS
# ============================================================

class Person:

    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight

    def print_info(self):
        print(f"Name   : {self.name}")
        print(f"Age    : {self.age}")
        print(f"Weight : {self.weight} kg")

    def get_older(self, years):
        self.age += years


# ============================================================
# 4. CREATE AND MANIPULATE AN OBJECT
# ============================================================

p1 = Person("Mike", 25, 89)

print("\nPERSON BEFORE:")
p1.print_info()

p1.get_older(6)

print("\nPERSON AFTER:")
p1.print_info()


# ============================================================
# 5. SAVE AN OBJECT USING PICKLE
# ============================================================

pickle_file ="mike.pickle"

# Save object
with open(pickle_file, "wb") as file:
    pickle.dump(p1, file)

print(f"\nObject saved to {pickle_file}")


# ============================================================
# 6. LOAD AN OBJECT USING PICKLE
# ============================================================

with open(pickle_file, "rb") as file:
    p1 = pickle.load(file)

print("\nRESTORED PERSON:")
p1.print_info()
