class InventoryItem:
    """A class to demonstrate operator overloading for inventory management"""
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __repr__(self):
        return f"InventoryItem(name='{self.name}', quantity='{self.quantity}')"
    
    #Plus
    def __add__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return InventoryItem (self.name, self.quantity + other.quantity)
        raise ValueError("Cannot add items of different types.")
    
    #Substraction
    def __sub__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            if self.quantity >= other.quantity:
                return InventoryItem (self.name, self.quantity - other.quantity)
            raise ValueError("Cannot substract more than the available quantity.")
        raise ValueError("Cannot add items of different types.")
    
    #Multiplication
    def __mul__(self, factor):
        if isinstance(factor, (int, float)):
            return InventoryItem (self.name, self.quantity * factor)
        raise ValueError("Multiplicatoin number must be a number.")

    #Normal Division
    def __truediv__(self, factor):
        if isinstance(factor, (int, float)) and factor != 0:
            return InventoryItem (self.name, self.quantity / factor)
        raise ValueError("Division number must be a non-zero number.")
    
    #Comparaison operator
    def __eq__(self, other):
        if isinstance(other, InventoryItem):
            return self.name == other.name and self.quantity == other.quantity
        return False
    
    def __lt__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return self.quantity < other.quantity 
        raise Exception("Cannot compare items of different types.")

    def __gt__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return self.quantity > other.quantity 
        raise Exception("Cannot compare items of different types.")
    
#Create some inventory items
items1 = InventoryItem("Apple", 50)
items2 = InventoryItem("Apple", 30)
items3 = InventoryItem("Orange", 20)

#Adding quantities of the same item
result_add = items1 + items2
print(result_add) #Output: InventoryItem(name='Apple', quantity='80')

#Subtracting quantities of the same item
result_sub = items1 - items2
print(result_sub) #Output: InventoryItem(name='Apple', quantity='20')

#Multiplying item quantities by a factor
result_mul = items1 * 2
print(result_mul) #Output: InventoryItem(name='Apple', quantity='100')

#Comparing item quantities
print(items1 > items2) #Output: True
print(items1 == InventoryItem("Apple", 50)) #Output: True

#Trying to add of different types
try:
    result_invalid = items1 + items3
except ValueError as e:
    print(e) #Output: Cannot add items of different types.

#Trying to substract more than available quantity
try:
    result_invalid = items2 - items1
except ValueError as e:
    print(e) #Output: Cannot substract more than the available quantity.