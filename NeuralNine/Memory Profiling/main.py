from memory_profiler import profile, memory_usage


# ---------------------------------------------------------
# 1. Profile a function and display the result in the console
# ---------------------------------------------------------

@profile
def myfunction(list_size):
    # Create a list containing one million references to "hello"
    mylist = ['hello'] * list_size

    # Create another list containing one million references to "world"
    mylist2 = ['world'] * list_size

    # Delete mylist2
    del mylist2

    # Return the first list
    return mylist


# ---------------------------------------------------------
# 2. Profile a function and write the result to a log file
# ---------------------------------------------------------

log_file = open('memory.log', 'w+')


@profile(stream=log_file)
def myfunction2(list_size):
    # Create a list containing one million references to "hello"
    mylist = ['hello'] * list_size

    # Create another list containing one million references to "world"
    mylist2 = ['world'] * list_size

    # Delete mylist2
    del mylist2

    # Return the first list
    return mylist


# ---------------------------------------------------------
# 3. Function used with memory_usage()
# ---------------------------------------------------------

def myfunction3(list_size):
    # Create a list containing one million references to "hello"
    mylist = ['hello'] * list_size

    # Create another list containing one million references to "world"
    mylist2 = ['world'] * list_size

    # Delete mylist2
    del mylist2

    # Return the first list
    return mylist


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

if __name__ == '__main__':

    # Profile myfunction() and display the result in the console
    myfunction(1_000_000)

    # Profile myfunction2() and write the result to memory.log
    myfunction2(1_000_000)

    # Measure the memory usage of myfunction3()
    mem_usage = memory_usage(
        (myfunction3, (), {'list_size': 1_000_000})
    )

    # Display the memory measurements
    print("Memory usage:", mem_usage)

    # Close the log file
    log_file.close()
