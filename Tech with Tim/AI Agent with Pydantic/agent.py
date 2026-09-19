import os
from datetime import datetime

from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider


# Connect to the local Ollama model
model = OllamaModel(
    "qwen3:4b",
    provider=OllamaProvider(base_url="http://localhost:11434/v1")
)

NOTES_FILE = "notes.txt"


# Return the current date and time
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")


# Evaluate a basic math expression
def calculate(expression: str) -> str:
    """Evaluate a basic math expression, e.g. '23 * 7 + 1'."""
    if not set(expression) <= set("0123456789+-*/(). "):
        return "Error: only numbers and + - * / ( ) are allowed."

    try:
        return str(eval(expression))
    except Exception as error:
        return f"Error: {error}"


# Save a note to the local file
def save_note(note: str) -> str:
    """Save a short note so it can be recalled later."""
    with open(NOTES_FILE, "a", encoding="utf-8") as file:
        file.write(f"- {note}\n")
    return "Saved."


# Read all saved notes
def read_note() -> str:
    """Read back all previously saved notes."""
    if not os.path.exists(NOTES_FILE):
        return "No notes saved yet."

    with open(NOTES_FILE, encoding="utf-8") as file:
        return file.read()


# Create the local AI agent with its available tools
agent = Agent(
    model,
    tools=[get_current_time, calculate, save_note, read_note],
    instructions=(
        "You are a helpful personal assistant running 100% locally. "
        "Use your tools whenever they can help answer the question. "
        "Keep your answer short and friendly. "
    ),
)


# Run the assistant in a simple command-line loop
def main():
    print("Local agent ready! Type 'quit' to exit.\n")

    history = []

    while True:
        user_input = input("You: ")

        # Stop the program when the user types quit or exit
        if user_input.strip().lower() in ("quit", "exit"):
            break

        # Send the user message to the agent
        result = agent.run_sync(
            user_input,
            message_history=history
        )

        # Keep the conversation history for the next message
        history = result.all_messages()

        print(f"\nAgent: {result.output}\n")


# Start the program
if __name__ == "__main__":
    main()
