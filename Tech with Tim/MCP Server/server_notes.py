from fastmcp import FastMCP
import os

# Create an MCP server instance with a descriptive name.
mcp = FastMCP("AI Sticky Notes")

# Path to the file used to store all notes.
# The file is created in the same directory as this script.
NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")


def ensure_file():
    """
    Create the notes file if it does not already exist.
    This prevents file access errors when reading or writing notes.
    """
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            f.write("")


@mcp.tool()
def add_note(message: str) -> str:
    """
    Append a new note to the sticky note file.

    Args:
        message (str): The note content to be added.

    Returns:
        str: Confirmation message indicating the note was saved.
    """
    # Ensure the storage file exists before writing.
    ensure_file()

    # Append the new note as a new line.
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

    return "Note saved!"


@mcp.tool()
def read_notes() -> str:
    """
    Read and return all notes from the sticky note file.

    Returns:
        str: All notes as a single string separated by line breaks.
             If no notes exist, a default message is returned.
    """
    # Make sure the notes file exists before reading.
    ensure_file()

    # Read the entire file content.
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # Return a friendly message when there are no saved notes.
    return content or "No notes yet."


@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Get the most recently added note from the sticky note file.

    Returns:
        str: The last note entry. If no notes exist, a default message is returned.
    """
    # Ensure the notes file exists.
    ensure_file()

    # Read all lines to retrieve the last one.
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Return the latest note, or a default message if the file is empty.
    return lines[-1].strip() if lines else "No notes yet."


@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Generate a prompt asking the AI to summarize all current notes.

    Returns:
        str: A prompt string that includes all notes and asks for a summary.
             If no notes exist, a message will be shown indicating that.
    """
    # Ensure the notes file exists before reading.
    ensure_file()

    # Load all notes from the file.
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # If there are no notes, inform the user.
    if not content:
        return "There are no notes yet."

    # Build a prompt that can be sent to an AI model.
    return f"Summarize the current notes: {content}"


# Run the MCP server when this script is executed directly.
# The server listens for incoming MCP requests from compatible clients.
if __name__ == "__main__":
    mcp.run()