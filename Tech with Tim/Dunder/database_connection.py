class DatabaseConnection:
    """Simulate a database connection wwith context management."""
    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = False

    def __enter__(self):
        """Establish the connection"""
        self.connected = True
        print(f"Connected to the database '{self.db_name}'.")
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection."""
        self.connected = False
        print(f"Disconnected to the database '{self.db_name}'.")
        #Handle any execptions
        if exc_type:
            print(f"An execption occured: {exc_value}")
        return True #Suppresses execptions if they occur
    
with DatabaseConnection("ExempleDB") as db:
    print(f"Is connected ? {db.connected}")