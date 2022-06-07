import tweepy
import requests
import os
import pandas as pd

#tokens
api_key = os.environ.get('Twitter_API_Key')
api_secret = os.environ.get('Twitter_API_Secret')
access_token = os.environ.get('Twitter_Access_Token')
access_secret = os.environ.get('Twitter_Access_Secret')
bearer = os.environ.get('bearer_token')

client = tweepy.Client( bearer_token=bearer,
                        return_type=requests.Response,
                        wait_on_rate_limit=True)

query = 'from:elonmusk -is:retweet'
tweets = client.search_recent_tweets(query=query,
                                    tweet_fields=['author_id', 'created_at'],
                                     max_results=20)

all_tweets = tweets.json()
tweets_data = all_tweets['data']
df = pd.json_normalize(tweets_data)
print(df.head)

def main():
    pass

if __name__ == "__main__":
    main()