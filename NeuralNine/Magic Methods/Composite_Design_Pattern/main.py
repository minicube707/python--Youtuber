
# The Composite Design Pattern is a structural design pattern that allows you to compose objects into tree-like structures to represent part-whole hierarchies.
# It lets clients treat individual objects and groups of objects in the same way.

# In this pattern, both simple elements (called leaf nodes) and more complex elements (called composites) implement a common interface.
# This makes it possible to perform operations uniformly, regardless of whether you are working with a single object or a collection of objects.

# In Python, the Composite pattern is often implemented by defining a base class with common methods, and then creating leaf and
# composite classes that implement or extend this behavior. The composite class typically stores child objects and delegates operations to them.

# This pattern is especially useful for representing hierarchical structures such as file systems, organizational charts, or
# graphical user interfaces.
    
from abc import ABCMeta, abstractmethod, abstractstaticmethod

class IDepartement(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, employees):
        """implement in child class"""

    @abstractstaticmethod
    def print_departement():
        """implement in child class"""

class Accounting(IDepartement):

    def __init__(self, employees):
        self.employees = employees

    def print_departement(self):
        print(f"Accouting Departement: {self.employees}")

class Development(IDepartement):

    def __init__(self, employees):
        self.employees = employees

    def print_departement(self):
        print(f"Development Departement: {self.employees}")

class ParentDepartement(IDepartement):
    
    def __init__(self, employees):
        self.employees = employees
        self.base_employees = employees
        self.sub_depts = []

    def add(self, dept):
        self.sub_depts.append(dept)
        self.employees += dept.employees

    def print_departement(self):
        print(f"Parent Departement Base Employees: {self.base_employees}")
        for dept in self.sub_depts:
            dept.print_departement()
        print(f"Total number of employees: {self.employees}")

dept1 = Accounting(200)
dept2 = Development(170)

parent_dept = ParentDepartement(30)
parent_dept.add(dept1)
parent_dept.add(dept2)

parent_dept.print_departement()