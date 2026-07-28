
# The `__init__.py` file is used to turn a directory into a Python package and to control what is exposed when the package is imported.
# It can be empty, but it is often used to initialize the package, import commonly used modules or functions, and define the `__all__` variable.
# The `__all__` list specifies which modules or objects are imported when someone uses `from package import *`.
# This makes the package easier to use and helps organize its public interface by exposing only the intended modules, functions, or classes.


# Define which modules are imported when using:
# from othermodule import *
__all__ = ["second", "third"]

# Import the function "myfunction" from the "second" module
from .second import myfunction

# Import the function "myotherfunction" from the "third" module
from .third import myotherfunction