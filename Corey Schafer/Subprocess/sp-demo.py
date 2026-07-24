import subprocess
import os
import platform

# The subprocess module allows a Python program to start and manage external programs.
# It provides a simple and flexible way to execute system commands, launch applications,
# and interact with other executables directly from Python.
# A subprocess can run synchronously, where Python waits for it to finish,
# or asynchronously, allowing multiple programs to run at the same time.
# The module also makes it possible to capture standard output and error streams,
# redirect input and output, communicate with running processes, and inspect
# their exit status. It is commonly used for automation, system administration,
# and integrating Python with command-line tools.

# ============================================================
# CPU Information
# Displays information about the current system and the
# available CPUs. Subprocesses are managed by the operating
# system and can run independently of the Python interpreter.
# ============================================================
print("=" * 60)
print("Display information about the current system.")
print("=" * 60)

print("CPU Information")
print(f"Operating System: {platform.system()} {platform.release()}")
print(f"Logical CPUs    : {os.cpu_count()}")
    
# ============================================================
# Example 1: Run a command using the shell
# shell=True executes the command through the system shell.
# This enables shell features such as pipes, redirections,
# wildcard expansion, and environment variable substitution.
# ============================================================
print("\n" + "=" * 60)
print("1. Run a command using the shell")
print("=" * 60)

# shell=True allows shell features such as pipes, redirections,
# wildcard expansion, and environment variable substitution.
print("Print IP adrress")
subprocess.run("hostname -I", shell=True)

# Example of a shell pipeline.
print("\nTop 10 memory-consuming processes")
subprocess.run("ps aux | sort -rk 4 | head -10", shell=True)


# ============================================================
# Example 2: Run a command without a shell (recommended)
# Passing the command as a list of arguments is safer and
# avoids shell injection vulnerabilities.
# ============================================================
print("\n" + "=" * 60)
print("2. Run a command without a shell (recommended)")
print("=" * 60)

# Passing a list of arguments is the recommended and safer approach.
print("ls -la")
subprocess.run(["ls", "-la"])


# ============================================================
# Example 3: Capture command output
# capture_output=True captures both stdout and stderr.
# By default, they are returned as bytes unless text=True
# is specified.
# ============================================================
print("\n" + "=" * 60)
print("3. Capture command output")
print("=" * 60)

# Capture stdout and stderr as bytes.
result = subprocess.run(["ls", "-la"], capture_output=True)

print("\n")
print(f"Args        : {result.args}")
print(f"Return code : {result.returncode}")
print(f"Stdout      : {result.stdout}")
print(f"Stderr      : {result.stderr}")

# text=True automatically decodes stdout and stderr into strings.
print("\nUsing text=True")
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)

print(result.stdout)


# ============================================================
# Example 4: Capture stdout using PIPE
# stdout=subprocess.PIPE explicitly redirects the standard
# output of the child process to the parent process.
# ============================================================
print("\n" + "=" * 60)
print("4. Using stdout=PIPE")
print("=" * 60)

# stdout=subprocess.PIPE explicitly captures the standard output.
result = subprocess.run(["ls", "-la"], stdout=subprocess.PIPE, text=True)

print(result.stdout)


# ============================================================
# Example 5: Redirect output to a file
# Standard output can be redirected directly to a file
# instead of being displayed in the terminal.
# ============================================================
print("\n" + "=" * 60)
print("5. Redirect output to a file")
print("=" * 60)

# Redirect stdout directly into a file.
with open("output.txt", "w") as file:
    subprocess.run(["ls", "-la"], stdout=file, text=True)

# Read the generated file.
with open("output.txt") as file:
    print(file.read())


# ============================================================
# Example 6: Handle command errors
# The return code indicates whether the command succeeded.
# Using check=True raises an exception when the command
# exits with a non-zero status.
# ============================================================
print("\n" + "=" * 60)
print("6. Error handling")
print("=" * 60)

# This command will fail because the directory does not exist.
result = subprocess.run(["ls", "-la", "does_not_exist"], capture_output=True, text=True)

print(f"Return code : {result.returncode}")
print(f"Error       : {result.stderr}")

# Raise a CalledProcessError if the command exits with a non-zero status.
# subprocess.run([...], check=True)


# ============================================================
# Example 7: Ignore standard error
# stderr can be redirected to DEVNULL to suppress
# error messages produced by the command.
# ============================================================
print("\n" + "=" * 60)
print("7. Ignore stderr")
print("=" * 60)

# Discard error messages by redirecting stderr to DEVNULL.
subprocess.run(["ls", "-la", "does_not_exist"], stderr=subprocess.DEVNULL)


# ============================================================
# Example 8: Simulate a pipe without the shell
# Capture the output of one command and pass it as the input
# of another command without relying on shell pipelines.
# ============================================================
print("\n" + "=" * 60)
print("8. Simulate a pipe without using the shell")
print("=" * 60)

# Execute the first command and capture its output.
cat = subprocess.run(["cat", "test.txt"], capture_output=True, text=True)

# Pass the captured output as the input of another command.
grep = subprocess.run(["grep", "-n", "test"], input=cat.stdout, capture_output=True, text=True)

print(grep.stdout)


# ============================================================
# Example 9: Create a real pipe between processes
# Popen allows multiple processes to run concurrently and
# communicate through pipes, similar to a shell pipeline.
# ============================================================
print("\n" + "=" * 60)
print("9. Create a real pipe between two processes")
print("=" * 60)

# Start the first process and connect its stdout to a pipe.
p1 = subprocess.Popen(["cat", "test.txt"], stdout=subprocess.PIPE, text=True)

# Connect the stdout of the first process to the stdin of the second.
p2 = subprocess.run(["grep", "-n", "test"], stdin=p1.stdout, capture_output=True, text=True)

# Close the pipe after it is no longer needed.
p1.stdout.close()

print(p2.stdout)