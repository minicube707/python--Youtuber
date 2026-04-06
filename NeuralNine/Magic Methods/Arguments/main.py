
# In Python, arguments are the values passed to a function when it is called.
# They allow functions to receive input and operate on different data, making code more flexible and reusable.

# Python supports several types of arguments, including positional arguments, keyword arguments, default arguments, and
# variable-length arguments (*args and **kwargs). Positional arguments are assigned based on their order,
# while keyword arguments are passed using parameter names, improving readability.
# Default arguments provide predefined values if no argument is given, and variable-length arguments allow functions to accept an arbitrary number of inputs.

# Understanding how to use these different types of arguments is essential for writing clean, adaptable, and maintainable Python code.
    
import sys
import getopt

# This function demonstrates the use of *args and **kwargs
def myfunction(*args, **kwargs):
    # *args collects positional arguments into a tuple
    print(args[0])
    print(args[1])
    print(args[2])
    print(args[3])

    # **kwargs collects keyword arguments into a dictionary
    print(kwargs['KEYONE'])
    print(kwargs['KEYTWO'])


print("\nARGS, KWARGS")

# Passing positional and keyword arguments
myfunction('hey', True, 19, 'wow', KEYONE="TEST", KEYTWO=7)


print("\nSYS")

# sys.argv is a list of command-line arguments
# argv[0] is the script name, the rest are arguments passed by the user
print(sys.argv)

# Looping through all command-line arguments
for i in range(len(sys.argv)):
    print(sys.argv[i])


print("\nGETOPT")

# getopt is used to parse command-line options and arguments
# sys.argv[1:] skips the script name
# "f:m:" means:
#   -f requires a value
#   -m requires a value
# ['filename', 'message'] are long option names (not used with '--' here)
opts, args = getopt.getopt(sys.argv[1:], "f:m:", ['filename', 'message'])

# opts = list of (option, value) pairs
# args = remaining arguments that were not parsed
print(opts)
print(args)


# Initialize variables
filename = ""
message = ""

# Loop through parsed options
for opt, arg in opts:
    if opt == '-f':
        filename = arg
    
    if opt == '-m':
        message = arg

# Display extracted values
print(f"filename: {filename}, message: {message}")