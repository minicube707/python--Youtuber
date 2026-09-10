import pandas as pd
from transformers import pipeline
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification


# Pre-trained DistilBERT model used for sentiment analysis
# Model: https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english
#
# Dataset used for the analysis:
# https://www.kaggle.com/datasets/odins0n/top-20-play-store-app-reviews-daily-update?select=Dropbox.csv


# Load the Dropbox reviews dataset from the CSV file
df = pd.read_csv('Dropbox.csv')

# Randomly select 200 reviews from the dataset
# This allows us to work with a smaller sample of the data
df = df.sample(200)


# Load the DistilBERT tokenizer
# The tokenizer converts text into tokens that can be processed by the model
tokenizer = DistilBertTokenizer.from_pretrained(
    'distilbert-base-uncased-finetuned-sst-2-english'
)

# Load the pre-trained DistilBERT model
# The model is already fine-tuned for sentiment classification
model = DistilBertForSequenceClassification.from_pretrained(
    'distilbert-base-uncased-finetuned-sst-2-english'
)


# Create a sentiment analysis pipeline
# The pipeline combines the tokenizer and the model to make predictions easier
nlp = pipeline(
    'sentiment-analysis',
    model=model,
    tokenizer=tokenizer
)


# Extract the review texts from the 'content' column
# Convert the values into a Python list
texts = list(df.content.values)


# Run sentiment analysis on all the reviews
# Each review will be classified as either POSITIVE or NEGATIVE
results = nlp(texts)


# Display the original review, the predicted sentiment, and the review score
for text, result, score in zip(texts, results, df.score.values):
    print('\n' + '=' * 30)
    print('Text: ', text)
    print('Result: ', result)
    print('Score: ', score)


# Add the predicted sentiment as a new column in the DataFrame
df['sentiment'] = [r['label'] for r in results]

# Display the sentiment column
print(df['sentiment'])
