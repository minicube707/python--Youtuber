import requests

# from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama


# ============================================================
# 1. MODEL CONFIGURATION
# ============================================================

# Name of the model installed and available in Ollama.
MODEL = "qwen3.5:9b"

# Create a ChatOllama instance.
# ChatOllama is a LangChain wrapper that allows us
# to communicate with an LLM running locally through Ollama.

model = ChatOllama(
    model=MODEL,

    # Temperature controls how creative or random
    # the model's responses can be.
    # 0 means that the model will generally try to be
    # as deterministic and consistent as possible.

    temperature=0
)


# ============================================================
# 2. ALTERNATIVE MODEL CONFIGURATION
# ============================================================

# Another way to initialize a chat model is by using
# LangChain's init_chat_model function.
#
# In this example, it is commented out because we are
# currently using ChatOllama with a local model.
#
# from langchain.chat_models import init_chat_model
#
# model = init_chat_model(
#     model='gpt-4.1-mini',
#     temperature=0.1
# )


# ============================================================
# 3. SEND A MESSAGE TO THE MODEL
# ============================================================

# invoke() sends a message to the language model
# and waits for its response.
#
# Here, we simply ask the model:
# "Hello, what is Python?"
response = model.invoke(
    'Hello, what is Python ?'
)


# ============================================================
# 4. DISPLAY THE RAW RESPONSE
# ============================================================

# Print the complete response object returned by LangChain.
# This object contains more than just the model's text.
# It can also contain metadata, response information,
# and other details about the generated message.

print("\n" + 60 * "=")
print("Raw Response:")
print(response)


# ============================================================
# 5. DISPLAY ONLY THE MODEL'S TEXT
# ============================================================

# The response object contains a "content" attribute.
# response.content gives us only the text generated
# by the language model, without the additional metadata.

print("\nClean Response:")
print(response.content)