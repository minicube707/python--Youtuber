import subprocess


#============================================================
print("=" * 60)
print("1. Run a command using the shell")
print("=" * 60)

# shell=True allows shell features such as pipes, redirections,
# wildcard expansion, and environment variable substitution.
print("Print IP adrress")
subprocess.run("hostname -I", shell=True)

# Example of a shell pipeline.
print("\nTop 10 memory-consuming processes")
subprocess.run("ps aux | sort -rk 4 | head -10", shell=True)


#============================================================
print("\n" + "=" * 60)
print("2. Run a command without a shell (recommended)")
print("=" * 60)

# Passing a list of arguments is the recommended and safer approach.
print("ls -la")
subprocess.run(["ls", "-la"])


#============================================================
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


#============================================================
print("\n" + "=" * 60)
print("4. Using stdout=PIPE")
print("=" * 60)

# stdout=subprocess.PIPE explicitly captures the standard output.
result = subprocess.run(["ls", "-la"], stdout=subprocess.PIPE, text=True)

print(result.stdout)


#============================================================
print("\n" + "=" * 60)
print("5. Redirect output to a file")
print("=" * 60)

# Redirect stdout directly into a file.
with open("output.txt", "w") as file:
    subprocess.run(["ls", "-la"], stdout=file, text=True)

# Read the generated file.
with open("output.txt") as file:
    print(file.read())


#============================================================
print("\n" + "=" * 60)
print("6. Error handling")
print("=" * 60)

# This command will fail because the directory does not exist.
result = subprocess.run(["ls", "-la", "does_not_exist"], capture_output=True, text=True)

print(f"Return code : {result.returncode}")
print(f"Error       : {result.stderr}")

# Raise a CalledProcessError if the command exits with a non-zero status.
# subprocess.run([...], check=True)


#============================================================
print("\n" + "=" * 60)
print("7. Ignore stderr")
print("=" * 60)

# Discard error messages by redirecting stderr to DEVNULL.
subprocess.run(["ls", "-la", "does_not_exist"], stderr=subprocess.DEVNULL)


#============================================================
print("\n" + "=" * 60)
print("8. Simulate a pipe without using the shell")
print("=" * 60)

# Execute the first command and capture its output.
cat = subprocess.run(["cat", "test.txt"], capture_output=True, text=True)

# Pass the captured output as the input of another command.
grep = subprocess.run(["grep", "-n", "test"], input=cat.stdout, capture_output=True, text=True)

print(grep.stdout)


#============================================================
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