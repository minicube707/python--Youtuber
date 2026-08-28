from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from transformers.utils.logging import set_verbosity_error

# Disable unnecessary Transformers logs
set_verbosity_error()


# ---------------------------------------------------------
# SUMMARIZATION PIPELINE
# ---------------------------------------------------------

# Load the BART model specialized in summarization.
# device=0 tells Transformers to use the first CUDA GPU.
summarization_pipeline = pipeline(
    task="summarization",
    model="facebook/bart-large-cnn",
    device=0
)

# Convert the Hugging Face pipeline into a LangChain LLM.
summarizer = HuggingFacePipeline(
    pipeline=summarization_pipeline
)


# ---------------------------------------------------------
# QUESTION ANSWERING PIPELINE
# ---------------------------------------------------------

# Load a question-answering model based on RoBERTa.
# The model extracts answers directly from the provided context.
qa_pipeline = pipeline(
    task="question-answering",
    model="deepset/roberta-base-squad2",
    device=0
)


# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------

# Ask the user for the text to summarize.
text_to_summarize = input(
    "\nEnter text to summarize:\n"
)


# Ask the user for the desired summary length.
length = input(
    "\nEnter the length (short/medium/long): "
).lower()


# ---------------------------------------------------------
# SUMMARY LENGTH SETTINGS
# ---------------------------------------------------------

# Define the maximum number of generated tokens
# depending on the user's selected summary length.
length_settings = {
    "short": 30,
    "medium": 60,
    "long": 100
}

# Use medium length if the user enters an invalid value.
max_new_tokens = length_settings.get(length, 60)


# Check how many tokens the input contains before summarization.
tokens = summarization_pipeline.tokenizer(
    text_to_summarize,
    return_tensors="pt",
    truncation=False
)

input_tokens = tokens["input_ids"].shape[1]

print(f"\nInput tokens: {input_tokens}")

# BART-large-CNN supports a maximum sequence length of 1024 tokens.
if input_tokens > 1024:
    print("\n⚠️ The input is too long for BART-large-CNN.")
    exit(0)

# ---------------------------------------------------------
# GENERATE SUMMARY
# ---------------------------------------------------------

# Generate the summary directly with the Hugging Face pipeline.
# max_new_tokens controls the maximum length of the generated summary.
summary_result = summarization_pipeline(
    text_to_summarize,
    max_new_tokens=max_new_tokens,
    min_new_tokens=10
)

# Extract the generated text from the pipeline result.
summary = summary_result[0]["summary_text"]


# Display the generated summary.
print("\n🔹 Generated Summary:")
print(summary)


# ---------------------------------------------------------
# QUESTION ANSWERING LOOP
# ---------------------------------------------------------

# Allow the user to ask questions about the generated summary.
while True:

    question = input(
        "\nAsk a question about the summary "
        "(or type 'exit' to stop):\n"
    )

    # Stop the program when the user types "exit".
    if question.lower() == "exit":
        break

    # Use the summary as the context for the QA model.
    qa_result = qa_pipeline(
        question=question,
        context=summary
    )

    # Display the answer.
    print("\n🔹 Answer:")
    print(qa_result["answer"])