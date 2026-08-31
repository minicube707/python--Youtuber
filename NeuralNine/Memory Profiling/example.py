# Use the commande line to start profiling
# uv run mprof run --python .\example.py

# Use the commande line to plot the result
# uv run mprof plot

def myfunction(list_size):
    # Create a list containing one million references to "hello"
    mylist = ['hello'] * list_size

    # Create another list containing one million references to "world"
    mylist2 = ['world'] * list_size

    # Delete the second list
    del mylist2

    # Return the first list
    return mylist


if __name__ == '__main__':
    # Run the function with one million elements
    myfunction(1_000_000)
