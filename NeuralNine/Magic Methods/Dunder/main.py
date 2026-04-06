
# In Python, dunder methods (short for “double underscore methods”) are special methods whose names start and end with double underscores,
# such as __init__, __str__, or __len__. They are also known as magic methods because they allow developers to define how objects behave with built-in operations.

# These methods are automatically called by Python in specific situations. For example, __init__ is used to initialize a new object,
# __str__ defines how an object is represented as a string, and __add__ allows custom behavior for the + operator.

# Dunder methods enable operator overloading and customization of class behavior, making user-defined objects behave like built-in types.
# By implementing them, developers can create more intuitive and expressive code.

class Person:

    # __init__ is the constructor.
    # It is called automatically when a new object is created.
    # It initializes the object's attributes.
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # __del__ is the destructor.
    # It is called when the object is about to be destroyed (garbage collected).
    # Note: Its execution timing is not always predictable.
    def __del__(self):
        print("Object is being desconstructed!")
    

p = Person("Mike", 25)



class Vector:

    # __init__ initializes the vector with x and y values.
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # __add__ defines the behavior of the + operator.
    # It allows you to add two Vector objects together.
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    # __str__ defines the string representation of the object.
    # It is called when using print() or str().
    def __str__(self):
        return f"X:{self.x} Y:{self.y}"    
    
    # __len__ defines what happens when len() is called on the object.
    # It should normally return a meaningful size, but here it returns a fixed value.
    def __len__(self):
        return 10
    
    # __call__ allows the object to be called like a function.
    # Example: v3() will execute this method.
    def __call__(self):
        print("Hello! I was called!")


v1 = Vector(10, 20)
v2 = Vector(50, 60)
v3 = v1 + v2

print(v3.x)
print(v3.y)

print(v3)
print(len(v3))

v3()