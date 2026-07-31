import os
from dotenv import load_dotenv

# --- Loading Environment Variables ---
# By default, load_dotenv() will NOT override an existing system environment variable.
# If "API_KEY" is already set in your Windows/Linux OS settings,
# the value from the .env file will be ignored unless you use override=True.
# Use override=True if you want the .env file to take precedence over system variables.
# load_dotenv(override=True)

load_dotenv()

# --- System Environment Variables ---
# These are variables provided by the Operating System (Windows, Linux, or macOS).
# They are usually populated before your script even runs.

# Windows specific: Path to the user's profile directory
USERPROFILE = os.getenv("USERPROFILE")
print(f"System USERPROFILE (Windows): {USERPROFILE}\n")

# Linux/macOS specific: Home directory path
# We provide a default value "Default_Home" if the variable is not found by the OS.
HOME_PATH = os.getenv("HOME", "Default_Home")
print(f"System HOMEPATH (Linux/macOS): {HOME_PATH}\n")

# --- Application Specific Variables ---
# These are variables usually defined in your .env file for your specific project.

# Fetching the API Key (Example of a critical variable)
API_KEY = os.getenv("API_KEY")
print(f"Application API_KEY: {API_KEY}\n")

# Fetching User Information
USER_NAME = os.getenv("USER_NAME")
print(f"Application USER_NAME: {USER_NAME}\n")

ADDRESS_1 = os.getenv("ADDRESS_1")
print(f"Address 1: {ADDRESS_1}\n")

ADDRESS_2 = os.getenv("ADDRESS_2")
print(f"Address 2: {ADDRESS_2}\n")

EMAIL = os.getenv("EMAIL")
print(f"Email: {EMAIL}\n")