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
    """

    :return: Twitter API authentication client
    """
    client = tweepy.Client( bearer_token=bearer,
                        return_type=requests.Response,
                        wait_on_rate_limit=True)
    return client

def create_query(username):
    """

    :param username: Twitter handle
    :return: Twitter API query string
    """
    query = f'from:{username}'
    return query

def call_api(client, query):
    """

    :param client: Twitter API authentication client
    :param query: Twitter query string
    :return: API call data
    """
    tweets = client.search_recent_tweets(query=query,
                                    tweet_fields=['author_id', 'id', 'created_at','source'],
                                     max_results=1000)
    return tweets

def data_to_df(data):
    """

    :param data: API call data
    :return: Pandas dataframe of data
    """
    all_tweets = data.json()
    tweets_data = all_tweets['data']
    df = pd.json_normalize(tweets_data)
    return df

def df_to_csv(df):
    """

    :param df: Pandas dataframe
    :return: CSV file of dataframe
    """
    df.to_csv('data.csv', encoding='utf-8', index=False)

def main():
    client = create_client()
    query = create_query('elonmusk')
    data = call_api(client,query)
    df = data_to_df(data)
    print(df)
    df_to_csv(df)

if __name__ == "__main__":
    main()