class MyClass:
    class_variable = "I am a class variable"

    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

    @classmethod
    def print_class_variable(cls):
        print(cls.class_variable)

    @staticmethod
    def add(x, y):
        return x + y
    
    def display(self):
        print("My name is", self.name ," and I ", self.age, " years old")

#Création de l'instance obj
obj =  MyClass("Harry", 23)   

# Appel à partir d'une instance
obj.display()

#@classmethod
# Appel à partir de la classe
MyClass.print_class_variable()

# Appel à partir d'une instance
obj.print_class_variable()

#@staticmethod
# Appel à partir de la classe
result = MyClass.add(3, 5)

# Appel à partir d'une instance (techniquement possible mais non recommandé)
result = obj.add(3, 5)
print(result)