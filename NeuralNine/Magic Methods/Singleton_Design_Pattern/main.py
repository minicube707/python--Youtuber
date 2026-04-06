
# The Singleton Design Pattern is a creational design pattern that ensures a class has only one instance and provides a global point of access to that instance.
# Instead of allowing multiple objects to be created, the class controls its own instantiation process and returns the same instance every time it is requested.

# This pattern is useful when exactly one object is needed to coordinate actions across a system, such as a configuration manager, logger,
# or database connection.

# In Python, the Singleton can be implemented in several ways, such as overriding the __new__ method,
# using a class variable to store the instance, or even using decorators or modules.
# While it is simple to implement, it should be used carefully, as it can introduce global state and make testing more difficult.

from abc import ABCMeta, abstractstaticmethod

class IPerson(metaclass=ABCMeta):

    @abstractstaticmethod
    def print_data():
        """implement in child class"""

class PersonSingleton(IPerson):

    __instance = None

    @staticmethod
    def get_instance():
        if PersonSingleton.__instance == None:
            PersonSingleton("Default Name", 0)
        return PersonSingleton.__instance
    
    def __init__(self, name, age):
        if PersonSingleton.__instance != None:
            raise Exception("Singleton cannot be instantiated more than once")


        else:
            self.name = name
            self.age = age
            PersonSingleton.__instance = self
    
    @staticmethod
    def print_data():
        print(f"Name: {PersonSingleton.__instance.name}, Age: {PersonSingleton.__instance.age}")

p = PersonSingleton("Mike", 30)
print(p)
p.print_data()

p2 = PersonSingleton.get_instance()
print(p2)
p2.print_data()

# p3 = PersonSingleton("Jack", 42)