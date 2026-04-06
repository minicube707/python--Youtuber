
# The Factory Design Pattern is a creational design pattern that provides an interface for creating objects without specifying their exact class.
# Instead of instantiating objects directly, a factory method is used to create and return the appropriate object based on given input.
# This helps improve code flexibility, scalability, and separation of concerns.

# In Python, although there is no strict concept of interfaces like in some other languages,
# developers often use abstract base classes (via the abc module) to define interface-like behavior.
# These classes declare methods that must be implemented by subclasses, ensuring a consistent structure across different implementations.

# Combining factory patterns with abstract base classes allows developers to build systems that are easy to extend and maintain,
# as new object types can be added with minimal changes to existing code.

from abc import ABCMeta, abstractstaticmethod

class IPerson(metaclass=ABCMeta):

    @abstractstaticmethod
    def person_method():
        """Interface Method"""

class Student(IPerson):

    def __init__(self):
        self.name = "Basic Student Name"

    def person_method(self):
        print("I am a student")

class Teacher(IPerson):
    
    def __init__(self):
         self.name = "Basic Teacher Name"

    def person_method(self):
        print("I am a teacher")


class PersonFactory:

    @staticmethod
    def  build_person(person_type):

        if person_type == "Student":
            return Student()
        
        if person_type == "Teacher":
            return Teacher()
        
        print("Invalid Type")
        return -1



s1 = Student()
t1 = Teacher()

s1.person_method()
t1.person_method()


if __name__ == "__main__":

    choice = input("What type do you want to create ?\n")
    person = PersonFactory.build_person(choice)
    person.person_method()