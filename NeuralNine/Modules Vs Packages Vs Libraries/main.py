
### 1. What is a Library?

# A **Library** is the broadest concept; it refers to a comprehensive collection of pre-written code, functions, classes, and modules designed to
# perform specific tasks. Think of a library as a massive toolbox filled with tools and blueprints—for example, the entire Python ecosystem or the
# extensive set of mathematical functions available in a data science package. Libraries provide the foundational knowledge and tools that programmers
# use to build larger applications without having to write every single piece of code from scratch.

### 2. What is a Package?

# A **Package** acts as an organizational container for related modules. If the library is the entire toolbox, the package is like a specific drawer or
# filing cabinet within that box, designed to group tools that work together. A package groups related functionalities into one logical unit, making it
# easier for developers to manage, distribute, and import large sets of related code seamlessly. It serves as an intermediary layer between the general
# library and the specific function.

### 3. What is a Module?

# A **Module** is the most fundamental and smallest unit of code—it is essentially a single file containing definitions for functions, classes, and
# variables that perform a specific task. If the package is the drawer (the container), the module is a single recipe card or tool inside that drawer.
# Modules represent the actual executable logic of a program; they are the smallest components that programmers write to define a specific operation,
# such as calculating a sum or handling a file input.

### 4. What is the Difference Between Them?

# The difference lies entirely in **scope and hierarchy**. The relationship is nested: a **Library** is the overarching collection of tools; a
# **Package** groups related Modules together into a logical container; and a **Module** is the specific, independent file or unit of code that contains
# the actual executable logic. In short: A Library is the big set, the Package organizes parts of that set, and the Module is the individual building
# block within those organized parts.

# ==============================================================
# SECTION 1: Importing Modules (Demonstrating complex importing)
# This section imports modules from a custom library called 'MyLib'.
# ==============================================================

import MyLib  # Import the main library namespace

# Import the entire Package1 module directly into the current scope
import MyLib.Package1

# Import the Package1 module using the 'from' statement (useful for clarity)
from MyLib import Package1

# Import a specific module ('module1') from within Package1
from MyLib.Package1 import module1

# Import a specific function ('myfunction1') from within 'module1'
from MyLib.Package1.module1 import myfunction1, myfunction2


# Call the imported function and print its result to the console
# This demonstrates that we successfully accessed the function defined in the nested file.


from MyLib.Package1 import module2
from MyLib.Package2 import module3
from MyLib.Package3 import module4

print("")
print(myfunction1())
print(MyLib.Package1.module2.myfunction3())

print("")
print(module3.myfunction5())
print(module3.myfunction6())

print("")
print(MyLib.Package3.module4.myfunction7())
print(MyLib.Package3.module4.myfunction8())
################

# ==============================================================
# SECTION 2: Example if Matplotlib (Setting up plotting environment)
# This section imports libraries necessary for creating graphs and plots.
# ==============================================================

import matplotlib # Import the core plotting library
import matplotlib.backends.backend_qt # Import a backend, likely used for integrating Matplotlib into a PyQt/Qt application

# Future code would typically follow here to define a plot using these imports.