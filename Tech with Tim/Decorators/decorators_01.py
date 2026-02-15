import time

#Decorator
#A decorator is a function that takes another function as argument
#and extends or modifies its behavior without changing its source code.

#Declare the decorator
def timer (func):
    #The decorator function.
    #It receives the function to decorate (func) as argument.

    def wrapper(*args, **kwargs):
        #The wrapper function replaces the original function.
        #It can execute code before and/or after calling the original function.
        #*args and **kwargs allow the wrapper to accept any arguments.

        start_time = time.time() #Start time
        result = func(*args, **kwargs) #Call the decorated function
        end_time = time.time() #End time
        print(f"Function {func.__name__!r} took: {end_time - start_time:.4f} sec")

        # Return the original function's result
        return result
    
     # Return the wrapper instead of the original function
    return wrapper

@timer
def example_function(n):
    #Example function that calculates the sum of numbers from 0 to n-1.
    return f"The sum is {sum(range(n))}"

print(example_function(1000000))

# Same as writing manually:
example_function = timer(example_function)

print("")
print(example_function(1000000))