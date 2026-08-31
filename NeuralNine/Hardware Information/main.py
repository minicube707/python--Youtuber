import platform

import psutil
import cpuinfo
import wmi


# ============================================================
# System Information
# ============================================================

print("=" * 60)
print("SYSTEM INFORMATION")
print("=" * 60)

# Get the system architecture (32-bit or 64-bit)
architecture = platform.architecture()[0]
print(f"Architecture     : {architecture}")

# Get the computer/network hostname
hostname = platform.node()
print(f"Computer Name    : {hostname}")

# Get a human-readable description of the operating system
operating_system = platform.platform()
print(f"Operating System : {operating_system}")

# Get the processor information reported by the platform module
processor = platform.processor()
print(f"Processor        : {processor}")


# ============================================================
# CPU Information
# ============================================================

print("\n" + "=" * 60)
print("CPU INFORMATION")
print("=" * 60)

# Get detailed CPU information using py-cpuinfo
cpu_info = cpuinfo.get_cpu_info()

# Display the full CPU brand/model name
cpu_name = cpu_info.get("brand_raw", "Unknown")
print(f"CPU Name         : {cpu_name}")

# Display all available CPU information
print("\nDetailed CPU Information:")

for key, value in cpu_info.items():
    print(f"{key:25}: {value}")


# ============================================================
# RAM Information
# ============================================================

print("\n" + "=" * 60)
print("MEMORY INFORMATION")
print("=" * 60)

# Get virtual memory information
memory = psutil.virtual_memory()

# Total RAM in bytes
total_ram_bytes = memory.total

# Convert bytes to gigabytes
total_ram_gb = total_ram_bytes / (1024 ** 3)

print(f"Total RAM        : {total_ram_gb:.2f} GB")
print(f"Available RAM    : {memory.available / (1024 ** 3):.2f} GB")
print(f"Used RAM         : {memory.used / (1024 ** 3):.2f} GB")
print(f"RAM Usage        : {memory.percent:.1f}%")


# ============================================================
# Windows WMI Information
# ============================================================

print("\n" + "=" * 60)
print("WINDOWS HARDWARE INFORMATION")
print("=" * 60)

# Create a connection to Windows Management Instrumentation (WMI)
computer = wmi.WMI()


# ------------------------------------------------------------
# Operating System
# ------------------------------------------------------------

# Retrieve information about the installed Windows operating system
os_info = computer.Win32_OperatingSystem()[0]

print("\nOperating System:")
print(f"Name             : {os_info.Caption}")
print(f"Version          : {os_info.Version}")
print(f"Build Number     : {os_info.BuildNumber}")
print(f"Architecture     : {os_info.OSArchitecture}")


# ------------------------------------------------------------
# CPU
# ------------------------------------------------------------

# Retrieve information about the installed CPU
cpu = computer.Win32_Processor()[0]

print("\nCPU:")
print(f"Name             : {cpu.Name}")
print(f"Manufacturer     : {cpu.Manufacturer}")
print(f"Cores            : {cpu.NumberOfCores}")
print(f"Logical CPUs     : {cpu.NumberOfLogicalProcessors}")
print(f"Max Clock Speed  : {cpu.MaxClockSpeed} MHz")


# ------------------------------------------------------------
# GPU
# ------------------------------------------------------------

# Retrieve information about the installed graphics controller
gpu = computer.Win32_VideoController()[0]

print("\nGPU:")
print(f"Name             : {gpu.Name}")
print(f"Driver Version   : {gpu.DriverVersion}")
print(f"Video Processor  : {gpu.VideoProcessor}")

# AdapterRAM may be unavailable on some systems, so check it first
if gpu.AdapterRAM:
    vram_gb = gpu.AdapterRAM / (1024 ** 3)
    print(f"VRAM             : {vram_gb:.2f} GB")


# ============================================================
# End of Program
# ============================================================

print("\n" + "=" * 60)
print("SYSTEM INFORMATION COLLECTION COMPLETE")
print("=" * 60)
