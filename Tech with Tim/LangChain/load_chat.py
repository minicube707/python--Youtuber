import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

MODEL = "llama3.2"

# Load environment variables from the .env file
load_dotenv()


def get_chat_model():
    """
    Factory function that returns the appropriate chat model
    based on the PROVIDER environment variable.

    Supported providers:
    - "ollama": Uses a local Ollama model.
    - "openai": Uses the OpenAI API.

    If PROVIDER is not set, "ollama" is used by default.
    """
    # Read the provider from the environment (default: ollama)
    provider = os.getenv("PROVIDER", "ollama").lower()

    if provider == "openai":
        print("Using OpenAI model...")
        # Initialize the OpenAI chat model using the API key from the environment
        return ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    elif provider == "ollama":
        print("Using Ollama model...")
        # Initialize the local Ollama model
        # Additional parameters (e.g., temperature) can be added here
        return ChatOllama(model=MODEL)

    else:
        # Raise an error if the provider is not supported
        raise ValueError("Provider must be 'openai' or 'ollama'")