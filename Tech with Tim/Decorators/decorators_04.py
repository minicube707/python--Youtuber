class Person:
    # Class attribute (shared by all instances)
    species = "Homo sapiens"

    @classmethod
    def get_species(cls):
        #The @classmethod decorator defines a method
        #that receives the class itself as first argument (cls),
        #instead of an instance (self).
        #   It can access and modify class-level attributes.

        print(cls) # Prints the class itself (e.g., <class '__main__.Person'>)
        return cls.species
    
#Usage
# No instance needed
print(Person.get_species()) #Homo sapiens