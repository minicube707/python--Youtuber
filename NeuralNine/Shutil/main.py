
import shutil
from pathlib import Path


# Define source and destination paths
source_file = Path("first.txt")
destination_file = Path("second.txt")

source_dir = Path("source_dir")
destination_dir = Path("destination_dir")


# ---------------------------------------
# 0. Copy a file without metadata
# ---------------------------------------

shutil.copy(source_file, destination_file)

# ---------------------------------------
# 1. Copy a file with metadata
# ---------------------------------------

shutil.copy2(source_file, destination_file)


# ---------------------------------------
# 2. Copy an entire directory
# ---------------------------------------

shutil.copytree(
    source_dir,
    destination_dir,
    dirs_exist_ok=True
)


# ---------------------------------------
# 3. Copy a directory while ignoring specific files
# ---------------------------------------

def ignore_specific_files(directory, files):
    """Ignore files named first.txt."""
    return [
        filename
        for filename in files
        if filename == "first.txt"
    ]


shutil.copytree(
    source_dir,
    "backup_dir",
    ignore=ignore_specific_files
)


# ---------------------------------------
# 4. Move or rename a file
# ---------------------------------------

shutil.move("first.txt", "third.txt")

# Move a file into another directory
shutil.move("third.txt", "source_dir/third.txt")


# ---------------------------------------
# 5. Remove a directory and its contents
# ---------------------------------------

# WARNING: This permanently deletes the directory!
# shutil.rmtree("source_dir")


# ---------------------------------------
# 6. Get disk usage information
# ---------------------------------------

total, used, free = shutil.disk_usage("/")

print(f"Total: {total / (1024**3):.2f} GB")
print(f"Used: {used / (1024**3):.2f} GB")
print(f"Free: {free / (1024**3):.2f} GB")


# ---------------------------------------
# 7. Copy file metadata
# ---------------------------------------

shutil.copystat("one.txt", "second.txt")


# ---------------------------------------
# 8. Change file ownership
# ---------------------------------------

# Requires appropriate system permissions
# shutil.chown("one.txt", user="root")


# ---------------------------------------
# 9. Find an executable in the system PATH
# ---------------------------------------

python_path = shutil.which("python3")

if python_path:
    print(f"Python found: {python_path}")
else:
    print("Python not found")


# ---------------------------------------
# 10. Create a ZIP archive
# ---------------------------------------

shutil.make_archive(
    base_name="myarchive",
    format="zip",
    root_dir="myfiles"
)


# ---------------------------------------
# 11. Extract an archive
# ---------------------------------------

shutil.unpack_archive(
    filename="myarchive.zip",
    extract_dir="unpacked_dir",
    format="zip"
)
