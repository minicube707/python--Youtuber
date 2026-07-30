"""
Python Module Import Examples

This script demonstrates different ways to import modules in Python
and introduces a few useful modules from the Python Standard Library.
"""

# ==========================================================
# Different ways to import your own module
# ==========================================================

# Import the entire module
import my_module

# Import the module with an alias
import my_module as mm

# Import specific objects from the module
from my_module import find_index, test

# Import a specific object with an alias
from my_module import find_index as fi

# Import everything from the module (generally not recommended)
from my_module import *

# ==========================================================
# Standard Library imports
# ==========================================================

import sys
import random
import math
import datetime
import calendar
import os

# A fun Easter egg included with Python 🚀
import antigravity

# ==========================================================
# Add a custom directory to Python's module search path
# ==========================================================

# Uncomment this line if you want Python to search
# for modules in a custom directory.
# sys.path.append("/path/to/my/module")

# ==========================================================
# Sample data
# ==========================================================

courses = ["History", "Math", "Physics", "CompSci"]

# ==========================================================
# Using functions imported in different ways
# ==========================================================

print("\n" + "=" * 60)
print("Import function")
print("=" * 60)

print(my_module.find_index(courses, "Math"))
print(mm.find_index(courses, "Physics"))
print(find_index(courses, "CompSci"))
print(fi(courses, "History"))

# Variable imported from the module
print(test)

# ==========================================================
# Exploring Python's module search path
# ==========================================================

print("\n" + "=" * 60)
print("sys.path")
print("=" * 60)

for path in sys.path:
    print(path)

print("\nExplanation:")
print("-" * 60)

# sys.path[0]
print("sys.path[0]")
print("-> Directory containing the script being executed.")
print("-> Python looks here first when importing modules.\n")

# Search for the Standard Library
for path in sys.path:
    if path.endswith("Lib"):
        print("Standard Library")
        print(f"-> {path}")
        print("-> Contains built-in modules like:")
        print("   random, os, math, datetime, calendar, pathlib...")
        print()

# Search for site-packages
for path in sys.path:
    if "site-packages" in path:
        print("Third-party Packages")
        print(f"-> {path}")
        print("-> Contains packages installed with pip.")
        print("   Examples: numpy, pandas, requests, flask...")
        print()

# Search for DLLs
for path in sys.path:
    if "DLL" in path.upper():
        print("DLLs Directory")
        print(f"-> {path}")
        print("-> Contains compiled extension modules (.dll/.pyd).")
        print()

# Search for zip file
for path in sys.path:
    if path.endswith(".zip"):
        print("Python ZIP Archive")
        print(f"-> {path}")
        print("-> Some Python installations store part of the")
        print("   Standard Library inside a ZIP archive.")
        print()
# ==========================================================
# Display all currently loaded modules
# ==========================================================

# sys.modules is a dictionary that stores all modules
# currently loaded by the Python interpreter.
#
# - Key   : Module name
# - Value : Module object
#
# Python checks this dictionary before importing a module.
# If the module is already loaded, Python reuses it instead
# of loading it again.
    
print("\n" + "=" * 60)
print("Loaded Modules")
print("=" * 60)

for module_name, module in sys.modules.items():
    print(f"Module: {module_name}")
    print(f"Object: {module}")
    print()

# ==========================================================
# Random module
# ==========================================================

print("\n" + "=" * 60)
print("Random Choices")
print("=" * 60)

for _ in range(3):
    print(random.choice(courses))

# ==========================================================
# Math module
# ==========================================================

print("\n" + "=" * 60)
print("Math Module")
print("=" * 60)

radians = math.radians(90)
print(f"sin(90°) = {math.sin(radians)}")

# ==========================================================
# Datetime module
# ==========================================================

print("\n" + "=" * 60)
print("Datetime Module")
print("=" * 60)

today = datetime.date.today()
print(today)

# ==========================================================
# Calendar module
# ==========================================================

print("\n" + "=" * 60)
print("Calendar Module")
print("=" * 60)

print(f"2017 is leap year: {calendar.isleap(2017)}")
print(f"2020 is leap year: {calendar.isleap(2020)}")

# ==========================================================
# OS module
# ==========================================================

print("\n" + "=" * 60)
print("OS Module")
print("=" * 60)

# Current working directory
print("Current working directory:")
print(os.getcwd())

# ==========================================================
# File Location
# ==========================================================

print("\n" + "=" * 60)
print("File Location")
print("=" * 60)

# Python modules written in Python usually have a __file__ attribute.
# It tells us where the module is located on disk.

# Some built-in or compiled modules do not expose __file__.
# They are loaded directly by the Python interpreter.

# Location of the os module itself
print("\nLocation of the os module:")
print("random:", getattr(random, "__file__", "No __file__ attribute"))
print("os    :", getattr(os, "__file__", "No __file__ attribute"))
print("math  :", getattr(math, "__file__", "No __file__ attribute"))