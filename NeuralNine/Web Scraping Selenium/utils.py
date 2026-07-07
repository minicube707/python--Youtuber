
def get_env():
    
    try:
        with open(".env") as f:
            for line in f:
                if line.startswith("PATH="):
                    return line.split("=", 1)[1].strip().strip('"')
        
    except FileNotFoundError:
        print("Error: .env file not found")
        exit()

    print("Error: PATH not found in .env")
    exit()