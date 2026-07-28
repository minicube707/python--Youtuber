# Import individual functions from the "fonctionality" module
from fonctionality import add
from fonctionality import sub
from fonctionality import mul
from fonctionality import div

# Equivalent to importing all functions from the module
# from fonctionality import *

# Import everything from the "othermodule" package
from othermodule import *

# Import only the "fourth" module from the "submodule" package
from submodule import fourth

# Equivalent to:
# from othermodule import second
# from othermodule import third

# Call the imported mathematical functions
print(add(2, 3))
print(sub(2, 3))
print(mul(2, 3))
print(div(2, 3))

# Call functions from the imported modules
second.myfunction()
third.myotherfunction()
fourth.last_function()