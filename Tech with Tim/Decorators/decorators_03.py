class Math:

    # @staticmethod
    # Used to define a method inside a class that does NOT
    # require access to the instance (self) or the class (cls).
    # It behaves like a regular function, but belongs to the class namespace

    @staticmethod
    def add(x, y):
        #Static method to add two numbers.
        #Can be called directly from the class without creating an instance.
        return x + y

    @staticmethod
    def multiply(x, y):
        #Static method to multiply two numbers.
        #Does not depend on any class or instance data.
        return x * y
    
# Usage
# No need to instantiate the class (no Math() required)
print(Math.add(5, 7)) # 12
print(Math.multiply(3, 4)) # 12