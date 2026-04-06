
# Encapsulation is a fundamental concept in object-oriented programming that consists of restricting direct access
# to an object’s internal data and exposing it only through controlled interfaces.
# In Python, this is typically achieved using classes, properties, and naming conventions.

# Instead of allowing external code to modify attributes directly, encapsulation encourages the use of getter and
# setter methods (or `@property` and its setter) to control how data is accessed and updated. This makes it possible to add validation,
# enforce rules, or change internal implementation without affecting the rest of the program.

# Python does not enforce strict access modifiers like some other languages,
# but it uses naming conventions such as a single underscore (`_attribute`) to indicate “protected” members and
# double underscores (`__attribute`) for name mangling, which helps avoid accidental access.

# Encapsulation improves code safety, maintainability, and flexibility by clearly separating an object’s internal state from how it is used.
# It also helps prevent unintended side effects by ensuring that data is modified only in well-defined ways.

class Person:

    def __init__(self, name, age, gender):
        self.__name = name
        self.__age = age
        self.__gender = gender

    @property
    def Name(self):
        return self.__name
    
    @Name.setter
    def Name(self, value):
        if value == "Jay":
            self.__name = "Default"
        else:
            self.__name = value

    @staticmethod
    def mymethod():
        print("Hello World!")

p1 = Person("Mike", 20, 'm')
print(p1.Name)

p1.Name = "Bob"
print(p1.Name)

p1.Name = "Jay"
print(p1.Name)

print("\nStaticMethod")
Person.mymethod()
p1.mymethod()