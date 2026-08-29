import requests

# from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama


# ============================================================
# 1. MODEL CONFIGURATION
# ============================================================

# Name of the model installed and available in Ollama.
MODEL = "qwen3.5:9b"

# Create a ChatOllama instance.
# This object is used to send messages to the local
# language model through Ollama.

model = ChatOllama(
    model=MODEL,

    # A temperature of 0 makes the model's responses
    # more deterministic and less creative/random.
    temperature=0
)


# ============================================================
# 2. ALTERNATIVE MODEL CONFIGURATION
# ============================================================

# Another way to initialize a chat model is to use
# LangChain's init_chat_model() function.
#
# This example is commented out because we are currently
# using ChatOllama with a local Ollama model.
#
# model = init_chat_model(
#     model='gpt-4.1-mini',
#     temperature=0.1
# )


# ============================================================
# 3. STREAM THE MODEL RESPONSE
# ============================================================

# stream() generates the response progressively instead
# of waiting for the entire response to be generated.
#
# The model sends small pieces of text called "chunks".
#
# This is useful for chat applications because the user
# can see the response appearing progressively, just like
# in ChatGPT.

for chunk in model.stream("Hello, what is Python?"):

    # chunk.text contains the text generated in the current chunk.
    # Each chunk only contains a small part of the complete
    # response, so we print it immediately.

    print(chunk.text, end='', flush=True)

    # flush=True forces Python to display the text
    # immediately instead of waiting for the output buffer
    # to be filled.