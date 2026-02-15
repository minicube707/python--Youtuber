class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        #The @property decorator allows this method to be accessed
        #like an attribute (c.radius instead of c.radius()).
        #It is used here as a getter.

        """Get the radius of the circle"""
        print("called me")
        return self._radius
    
    @radius.setter
    def radius(self, value):
        #The @radius.setter decorator defines the setter method
        #for the 'radius' property.
        #It allows us to control and validate the value before setting it.

        """Set the radius of the circle. Must be positive."""
        if value >= 0:
            self._radius = value
        else:
            raise ValueError("radius must be positive")
        
    @property
    def diameter(self):
        #Another read-only property.
        #No setter is defined, so the diameter cannot be modified directly.
        #It is computed dynamically from the radius.

        """Get the diameter of the circle."""
        return self._radius * 2
    
    @radius.deleter
    def radius(self):
        #The @radius.deleter decorator defines behavior
        #when using 'del c.radius'.

        print("deleted")
        del self._radius
    
#Usage
c = Circle(5)
print(c.radius) #5
print(c.diameter) #10

c.radius = 10
print(c.radius) #10
print(c.diameter) #20

del c.radius