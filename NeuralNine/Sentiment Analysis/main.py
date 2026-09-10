from textblob import TextBlob
from newspaper import Article


# URLs of different articles that can be used for the analysis
# url = "https://en.wikipedia.org/wiki/Mathematics"
# url = "https://www.bbc.com/news/articles/c78xyw7pg8vo"
# url = "https://www.bbc.com/news/articles/cp3p5l0nyevo"
# url = "https://www.bbc.com/news/business-12297002"
# url = "https://www.bbc.com/news/articles/c98elnpr0kzo"
# url = "https://www.bbc.com/pidgin/world-58484932"


# Create an Article object using the selected URL
# article = Article(url)

# Download the article from the website
# article.download()

# Parse the downloaded article and extract its text
# article.parse()

# Perform natural language processing on the article
# article.nlp()

# Get the full text of the article
# text = article.text
# print("\n" + "=" * 60)
# print("Text:")
# print(text)


# Get the automatically generated summary of the article
# summary = article.summary
# print("\n" + "=" * 60)
# print("Summary:")
# print(summary)


# Perform sentiment analysis on the article summary
# print("\n" + "=" * 60)
# print("Sentiment:")
# blob = TextBlob(summary)

# Get the sentiment polarity score
# The score ranges from -1 (very negative) to 1 (very positive)
# sentiment = blob.sentiment.polarity
# print(sentiment)


# Open the file containing positive text
with open("positive.txt", 'r') as f:
    text = f.read()

# Calculate the sentiment polarity of the positive text
print("\n" + "=" * 60)
print("Sentiment:")

# Create a TextBlob object from the text
blob = TextBlob(text)

# Get the sentiment polarity score
# A positive value indicates a positive sentiment
sentiment = blob.sentiment.polarity
print(sentiment)


# Open the file containing negative text
with open("negative.txt", 'r') as f:
    text = f.read()

# Calculate the sentiment polarity of the negative text
print("\n" + "=" * 60)
print("Sentiment:")

# Create a TextBlob object from the text
blob = TextBlob(text)

# Get the sentiment polarity score
# A negative value indicates a negative sentiment
sentiment = blob.sentiment.polarity
print(sentiment)


# Open the file containing neutral text
with open("neutral.txt", 'r') as f:
    text = f.read()

# Calculate the sentiment polarity of the neutral text
print("\n" + "=" * 60)
print("Sentiment:")

# Create a TextBlob object from the text
blob = TextBlob(text)

# Get the sentiment polarity score
# A value close to 0 indicates a neutral sentiment
sentiment = blob.sentiment.polarity
print(sentiment)
