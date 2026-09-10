import feedparser
from transformers import pipeline


# Define the stock ticker and the keyword used to filter relevant articles
ticker = 'META'
keyword = 'meta'


# Load the FinBERT model for financial sentiment analysis
# FinBERT is specifically trained to analyze sentiment in financial texts
pipe = pipeline(
    task='text-classification',
    model='ProsusAi/finbert'
)


# Example of a sentiment analysis using FinBERT
# print(pipe('Stocks rallied and the British pound gained.'))


# Build the Yahoo Finance RSS feed URL using the stock ticker
rss_url = f'https://finance.yahoo.com/rss/headline?s={ticker}'


# Parse the RSS feed and retrieve the available news articles
feed = feedparser.parse(rss_url)


# Initialize variables to calculate the overall sentiment
# total_score stores the sum of positive and negative sentiment scores
# num_articles counts the number of articles used in the calculation
total_score = 0
num_articles = 0


# Loop through all articles available in the RSS feed
for i, entry in enumerate(feed.entries):

    # Skip articles that do not contain the specified keyword in their summary
    if keyword.lower() not in entry.summary.lower():
        continue


    # Display basic information about the article
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Published: {entry.published}")
    print(f"Summary: {entry.summary}")


    # Analyze the sentiment of the article summary using FinBERT
    # The model returns a sentiment label and a confidence score
    sentiment = pipe(entry.summary)[0]


    # Display the predicted sentiment and its confidence score
    print(f"Sentiment: {sentiment['label']}, Score: {sentiment['score']}")
    print('\n' + '-' * 40)


    # If the sentiment is positive, add its score to the total
    if sentiment['label'] == 'positive':
        total_score += sentiment['score']
        num_articles += 1


    # If the sentiment is negative, subtract its score from the total
    elif sentiment['label'] == 'negative':
        total_score -= sentiment['score']
        num_articles += 1


# Calculate the average sentiment score across all relevant articles
final_score = total_score / num_articles


# Classify the overall sentiment based on predefined thresholds
# Score >= 0.15  -> Positive
# Score <= -0.15 -> Negative
# Otherwise      -> Neutral
print(
    f'Overall Sentiment: '
    f'{"Positive" if final_score >= 0.15 else "Negative" if final_score <= -0.15 else "Neutral"} '
    f'{final_score}'
)
