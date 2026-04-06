
# Type hinting in Python is a way to indicate the expected data types of variables, function parameters, and return values.
# It does not enforce types at runtime, but it helps developers write clearer and more maintainable code.

# By specifying types (for example, def add(a: int, b: int) -> int:), you make your code easier to understand and reduce the risk of errors.
# Type hints are especially useful when working in teams, as they act as a form of documentation.

# They also enable better support from development tools such as linters, IDEs, and static type checkers like mypy,
# which can detect potential bugs before the code is executed.

# In short, type hinting improves code readability, helps catch mistakes early, and
# makes large codebases easier to manage without changing how Python executes the program.

def myfunction(myparameter: int) -> str:
    
    if (type(myparameter) == int):
        print("myparameters is an int")
        return "int"
    
    else:
        print("Error")
        return "error"


res = myfunction(42)
print(res)

res = myfunction("Hello World")
print(res)
