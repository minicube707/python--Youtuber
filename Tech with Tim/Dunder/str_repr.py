class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    #__str__ is meant for user-friendly output
    def __str__(self):
        return f"{self.year} {self.make} {self.model}"
    
    #__reper__ is meant for a more detail, unambigous output (representation methode, for debug)
    def __repr__(self): 
        return f"Car(make='{self.make}, model='{self.model}', year='{self.year}')"
    
#Create an istance of the Cars class
my_car = Car('Toyota', 'Corolla', 2021)

#Exemple
print(str(my_car))
print(repr(my_car))