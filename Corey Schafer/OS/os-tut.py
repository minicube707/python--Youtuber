import os
from datetime import datetime


#============================================================
print("=" * 60)
print("1. Explore the os module")
print("=" * 60)

# Display all available attributes and functions in the os module.
print(dir(os))


#============================================================
print("\n" + "=" * 60)
print("2. Get and change the current working directory")
print("=" * 60)

# Save the current working directory.
initial_pwd = os.getcwd()
print(initial_pwd)

# Change the current working directory.
os.chdir("/")
print(os.getcwd())

# List the contents of the current directory.
print(os.listdir())

# Restore the original working directory.
os.chdir(initial_pwd)


#============================================================
print("\n" + "=" * 60)
print("3. Create directories")
print("=" * 60)

# Create all missing parent directories.
# os.mkdir() creates only one directory.
# os.makedirs() creates nested directories.
# os.mkdir("OS-Demo-2/Sub-Dir-1")
os.makedirs("OS-Demo-2/Sub-Dir-1")


#============================================================
print("\n" + "=" * 60)
print("4. Rename files")
print("=" * 60)

# Rename a file.
os.rename("test.txt", "demo.txt")

print(os.listdir())


#============================================================
print("\n" + "=" * 60)
print("5. File information")
print("=" * 60)

# Retrieve file metadata.
stats = os.stat("demo.txt")

print(stats)

# Last modification time (Unix timestamp).
modification_time = stats.st_mtime
print(f"Time stamp of last modification: {modification_time}")

# Convert the timestamp into a readable date.
print(f"Time since last modification: {datetime.fromtimestamp(modification_time)}")


# Restore the original file name.
os.rename("demo.txt", "test.txt")


#============================================================
print("\n" + "=" * 60)
print("6. Walk through a directory tree")
print("=" * 60)

# Recursively iterate through all directories and files.
for dirpath, dirnames, filenames in os.walk("."):

    print("Current Path :", dirpath)
    print("Directories  :", dirnames)
    print("Files        :", filenames)
    print("-" * 40)


#============================================================
print("\n" + "=" * 60)
print("7. Environment variables")
print("=" * 60)

# Read the HOME environment variable.
print(os.environ.get("HOME"))


#============================================================
print("\n" + "=" * 60)
print("8. Remove directories")
print("=" * 60)

# os.rmdir() removes a single empty directory.
# os.removedirs() removes nested empty directories.
# os.rmdir("OS-Demo-2/Sub-Dir-1")
os.removedirs("OS-Demo-2/Sub-Dir-1")


#============================================================
print("\n" + "=" * 60)
print("9. Build file paths")
print("=" * 60)

# Build a platform-independent file path.
file_path = os.path.join(os.getcwd(), "test", "file_test.txt")
print(file_path)


#============================================================
print("\n" + "=" * 60)
print("10. Path manipulation")
print("=" * 60)

# Extract only the filename.
print(f"Base name: {os.path.basename("/tmp/test.txt")}")

# Extract only the directory.
print(f"Dir name: {os.path.dirname("/tmp/test.txt")}")

# Split a path into directory and filename.
print(f"Split: {os.path.split("/tmp/test.txt")}")


#============================================================
print("\n" + "=" * 60)
print("11. Path checks")
print("=" * 60)

# Check whether a path exists.
print(f"Path exit ?: {os.path.exists("/tmp/test.txt")}")

# Check whether the path is a directory.
print(f"Is dir ?: {os.path.isdir(".")}")

# Check whether the path is a file.
print(f"Is file ?: {os.path.isfile("test.txt")}")


#============================================================
print("\n" + "=" * 60)
print("12. File extension")
print("=" * 60)

# Split the filename from its extension.
print(f"Split extension: {os.path.splitext("/tmp/test.txt")}")


#============================================================
print("\n" + "=" * 60)
print("13. Explore os.path")
print("=" * 60)

# Display all available functions in os.path.
print(dir(os.path))