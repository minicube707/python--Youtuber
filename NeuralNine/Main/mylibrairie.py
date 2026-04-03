
def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def hello():
    print("Hello World")

def main():
    print("Inside main function")
    print("Program executed directly (not imported).")

    # Example of use
    a, b = 10, 5
    print(f"{a} + {b} = {add(a, b)}")
    print(f"{a} - {b} = {sub(a, b)}")

    hello()

print("Read by the interpreter, even I not execute")
print(f"__name__ = {__name__}")

# This block only executes if the file is launched directly
if __name__ == "__main__":
    print(f"__name__ = {__name__}")
    main()