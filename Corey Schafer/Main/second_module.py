# ============================================
# Example usage:
# --------------------------------------------
# python second_module.py
#     -> imports first_module
#     -> triggers its top-level code
#     -> prints names of both modules
# ============================================

# Import the first module
# This will execute all top-level code in first_module.py
import first_module

# Print the name of the current module
# Since this file is executed directly, it will be "__main__"
print("Second Module's Name: {}".format(__name__))