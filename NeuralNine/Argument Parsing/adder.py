import argparse
import time

# ============================================
# Example usage:
# --------------------------------------------
# python script.py "Hello world"
#     -> prints the greeting only
#
# python script.py "Hello" -n 3 5
#     -> prints "Hello" and the sum (8)
#
# python script.py "Hi" -n 2 4 -v 1
#     -> prints greeting, sum, and the numbers list
#
# python script.py "Hey" -n 1 2 -v 2 --debug
#     -> prints everything + extra info + execution time
# ============================================

# Create the argument parser object
parser = argparse.ArgumentParser()

# Positional argument: a greeting message to display
parser.add_argument('greeting', help="The greeting message displayed")

# Optional argument: two float numbers to add together
parser.add_argument('-n', '--numbers', type=float, nargs=2, help="The numbers to be added")

# Optional argument: controls how much information is displayed (0, 1, or 2)
parser.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2],
                    help="Determines how much info is displayed")

# Optional flag: enables debug mode (measures execution time)
parser.add_argument('--debug', action='store_true', help="Enables debug mode")

# Parse the command-line arguments
args = parser.parse_args()

# If debug mode is enabled, start timing
if args.debug:
    start = time.perf_counter()

# Print all parsed arguments (for inspection)
print(args)

# Print the numbers argument (if provided)
print(args.numbers)

# If no verbosity level is specified
if args.verbosity is None:

    # Always print the greeting
    print(args.greeting)

    # If numbers are provided, print their sum
    if args.numbers is not None:
        print(args.numbers[0] + args.numbers[1])

else:
    # Verbosity level 0 or higher: basic output
    if args.verbosity >= 0:
        print(args.greeting)
        if args.numbers is not None:
            print(args.numbers[0] + args.numbers[1])

    # Verbosity level 1 or higher: show the raw numbers
    if args.verbosity >= 1:
        print(args.numbers)

    # Verbosity level 2: extra debug/info output
    if args.verbosity >= 2:
        print("Extra info")

# If debug mode is enabled, stop timing and print execution duration
if args.debug:
    end = time.perf_counter()
    print(end - start)