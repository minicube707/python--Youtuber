import requests
from transformers import pipeline


# Read the NewsAPI key from the .env file
API_KEY = open('.env').read()


# Define the keyword and the date used to search for news articles
keyword = 'gold'
date = '2024-08-18'


# Load the FinBERT model for financial sentiment analysis
# FinBERT is designed to classify financial texts as positive, negative, or neutral
pipe = pipeline(
    task='text-classification',
    model='ProsusAi/finbert'
)


# Build the NewsAPI request URL
# The API searches for articles containing the specified keyword
# and sorts the results by popularity
url = (
    'https://newsapi.org/v2/everything?'
    f'q={keyword}&'
    f'from={date}&'
    'sortBy=popularity&'
    f'apiKey={API_KEY}'
)


# Send a GET request to NewsAPI
response = requests.get(url)


# Convert the API response from JSON format into a Python dictionary
# and extract the list of articles
articles = response.json()['articles']


# Keep only the articles where the keyword appears
# in either the title or the description
articles = [
    article for article in articles
    if keyword.lower() in article['title'].lower()
    or keyword.lower() in article['description'].lower()
]


# Initialize variables used to calculate the overall sentiment
# total_score stores the combined sentiment score
# num_articles counts the articles used in the calculation
total_score = 0
num_articles = 0


# Loop through all filtered articles
for i, article in enumerate(articles):

    # Display information about the current article
    print(f"Title: {article['title']}")
    print(f"Link: {article['url']}")
    print(f"Description: {article['description']}")


    # Analyze the content of the article using FinBERT
    # The model returns a sentiment label and a confidence score
    sentiment = pipe(article['content'])[0]


    # Display the sentiment prediction and its confidence score
    print(f"Sentiment: {sentiment['label']}, Score: {sentiment['score']}")
    print('\n' + '-' * 40)


    # Add the score if the sentiment is positive
    if sentiment['label'] == 'positive':
        total_score += sentiment['score']
        num_articles += 1


    # Subtract the score if the sentiment is negative
    elif sentiment['label'] == 'negative':
        total_score -= sentiment['score']
        num_articles += 1


# Calculate the average sentiment score
final_score = total_score / num_articles


# Determine the overall sentiment using predefined thresholds
# A score >= 0.15 is considered Positive
# A score <= -0.15 is considered Negative
# Any value between these thresholds is considered Neutral
print(
    f'Overall Sentiment: '
    f'{"Positive" if final_score >= 0.15 else "Negative" if final_score <= -0.15 else "Neutral"} '
    f'{final_score}'
)
