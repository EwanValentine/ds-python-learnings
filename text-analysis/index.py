import re
from textblob import TextBlob 

"""
Text sentiment analysis example.

I can't believe how easy this was.
"""

def get_sentiment(text):
  analysis = TextBlob(text)
  return analysis.sentiment

results = get_sentiment('What the fuck were Derby doing tonight? Utter shite mate.')
if results.polarity > 0:
  print("Positive")
elif results.polarity == 0:
  print("Neutral")
else:
  print("Negative")

print(results.polarity)
