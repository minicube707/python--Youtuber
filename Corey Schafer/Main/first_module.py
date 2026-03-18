# ============================================
# Example usage:
# --------------------------------------------
# python first_module.py
#     -> runs this file directly
#     -> prints module name as "__main__"
#     -> executes main()
#
# python second_module.py
#     -> imports this file
#     -> prints module name as "first_module"
#     -> does NOT execute main()
# ============================================

# Print the name of the current module
# "__main__" if run directly, otherwise the module name when imported
print("First Module's Name: {}".format(__name__))

# Define a main function that will only run when the script is executed directly
def main():
    print("Message from main function")

# Check if the script is being run directly (not imported)
if __name__ == "__main__":
    main()
else:
    # This block runs only when the module is imported
    print("Run from import/")