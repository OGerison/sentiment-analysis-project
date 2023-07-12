import tweepy
import re
import configparser
import pandas as pd

# read configs
config = configparser.ConfigParser()
config.read("config.ini")

api_key = config["twitter"]["api_key"]
api_key_secret = config["twitter"]["api_key_secret"]
access_token = config["twitter"]["access_token"]
access_token_secret = config["twitter"]["access_token_secret"]

#print(api_key)

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Set the hashtag to search for
hashtag = "Enter Hashtag"

# Use tweepy's Cursor object to fetch the tweets
tweets = tweepy.Cursor(api.search_tweets, q=hashtag, lang="en").items(100)

# Iterate through the tweets and clean the data
cleaned_tweets = []
for tweet in tweets:
  # Remove URLs
  text = re.sub(r"http\S+", "", tweet.text)
  
  # Remove special characters and hashtags
  text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
  
  # Remove extra whitespace
  text = re.sub(r"\s+", " ", text)
  
  # Append the cleaned tweet to the list
  cleaned_tweets.append(text)
print(cleaned_tweets)

# Create a dataframe from the cleaned tweets
df = pd.DataFrame({"tweet": cleaned_tweets})

# Display the dataframe
print(df)

# Save the dataframe to a CSV file
df.to_csv("data/cleaned_tweets.csv", index=True)
