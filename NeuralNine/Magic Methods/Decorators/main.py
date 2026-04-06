
# Decorators in Python are a powerful feature that allows you to modify or extend the behavior of a function without changing its actual code.
# A decorator is essentially a function that takes another function as input, wraps it inside another function, and returns the modified version.

# They are commonly used for cross-cutting concerns such as logging, timing, authentication, or access control.
# By using decorators, you can keep your core logic clean while adding reusable functionality in a modular way.

# The `@decorator_name` syntax is just a convenient shorthand for applying a decorator.
# For example, `@my_decorator` above a function is equivalent to calling `my_decorator(function)` manually.

# A typical decorator defines an inner function (often called `wrapper`) that can accept any arguments using `*args` and `**kwargs`, ensuring compatibility with different function signatures.
# It usually calls the original function, possibly adding behavior before and/or after the call.

# In short, decorators help you write cleaner, more maintainable, and reusable code by separating concerns and reducing duplication.


def mydecorator(function):

    def wrapper():
        print("I am decorating your function!")
        function()
    return wrapper

def hello_world():
    print("Hello World!")

@mydecorator
def hello_world_annotation():
    print("Hello World Annotatoin!")


print("\n--- Without decorator syntax ---")
mydecorator(hello_world)()

print("\n--- With decorator syntax ---")
hello_world_annotation()

#We have some limitation because if your fonction take arguments, 
#the program will crash because the decorators doesn't have arguments or the same arguments
#To fix it put *args and **kwargs to the anotation function

