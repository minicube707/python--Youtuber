from dataclasses import dataclass

class Product:
    #Traditional class implementation.
    #We manually define __init__, __repr__, and __eq__.

    def __init__(self, name: str, price: float, quantity: int = 0):
        # Instance attributes
        self.name = name
        self.price = price
        self.quantity = quantity

    def total_cost(self) -> float:
        #Regular instance method.
        #Calculates total cost based on price and quantity.
        return self.price * self.quantity
    
    def __repr__(self):
        #Defines the official string representation of the object.
        #Useful for debugging and printing.
        return (
            f"Product(name={self.name!r}, price={self.price}, quantity={self.quantity})"
        )
    
    def __eq__(self, other):
        #Defines how two Product objects are compared using ==.
        if not isinstance(other, Product):
            #don't attempt to campare against unrelated types
            return NotImplemented
        
        return (
            self.name == other.name
            and self.price == other.price
            and self.quantity == other.quantity
        )

@dataclass 
class Product2:

    #@dataclass automatically generates:
    #- __init__()
    #- __repr__()
    #- __eq__()
    #- and other utility methods
    #Based only on the class attributes defined below.

    name: str
    price: float
    quantity: int = 0

    def total_cost(self) -> float:
        #You can still define custom methods normally.
        return self.price * self.quantity

# ---- Usage with traditional class ---- 
p1 = Product(name="Laptop", price=1000.0, quantity=3)
p2 = Product(name="Laptop", price=1000.0, quantity=3)
p3 = Product(name="Smartphone", price=500.0, quantity=2)

print(p1)               # Uses custom __repr__
print(p1.total_cost())  # 3000.0
print(p1 == p2)          # True (uses custom __eq__)
print(p1 == p3)          # False

print("")

# ---- Usage with dataclass ----
p1 = Product2(name="Laptop", price=1000.0, quantity=3)
p2 = Product2(name="Laptop", price=1000.0, quantity=3)
p3 = Product2(name="Smartphone", price=500.0, quantity=2)

print(p1)               # Auto-generated __repr__
print(p1.total_cost())  # 3000.0
print(p1 == p2)         # True (auto-generated __eq__)
print(p1 == p3)         # False