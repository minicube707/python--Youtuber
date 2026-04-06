
#Practical exemple #1 -Logging

def logged(function):
    def wrapper(*args, **kwargs):
        value = function(*args, **kwargs)
        with open('logfile.txt', 'a+') as f:
            fname = function.__name__
            print(f"{fname} returned value {value}")
            f.write(f"{fname} returned value {value}")
        return value
    
    return wrapper

def add(x, y):
    return x + y

@logged
def add_logged(x, y):
    return x + y

print("Without log")
print(add(10, 20))

print("\nWith log")
add_logged(10, 20)