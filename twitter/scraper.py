import tweepy
import requests
import os
import pandas as pd

# global tokens
api_key = os.environ.get('Twitter_API_Key')
api_secret = os.environ.get('Twitter_API_Secret')
access_token = os.environ.get('Twitter_Access_Token')
access_secret = os.environ.get('Twitter_Access_Secret')
bearer = os.environ.get('bearer_token')

def create_client():
    client = tweepy.Client( bearer_token=bearer,
                        return_type=requests.Response,
                        wait_on_rate_limit=True)
    return client

def create_paginator(authenticated_client):

    paginator = tweepy.Paginator(
        authenticated_client.search_recent_tweets,
        query='from:elonmusk',
        tweet_fields=['author_id', 'id', 'created_at'],
        max_results=100,
        limit=5)

    return paginator

def main():
    client = create_client()

    for tweet in tweepy.Paginator(client.search_recent_tweets, "Tweepy",
                                  max_results=100).flatten(limit=250):
        print(tweet.id)

if __name__ == "__main__":
    main()