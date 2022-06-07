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
    '''
    Returns an authenticated client
    '''
    client = tweepy.Client( bearer_token=bearer,
                        return_type=requests.Response,
                        wait_on_rate_limit=True)
    return client

def get_user_id(authenticated_client, username):
    '''
    Takes an authenticated client, Twitter Handle.
    Returns a Response object
    '''
    response = authenticated_client.get_user(username=username)
    return response

def paginator_recent_tweets(authenticated_client, query):
    paginator = tweepy.Paginator(authenticated_client.search_recent_tweets, query=query,
                                  tweet_fields=['author_id', 'id', 'created_at'],max_results=100).flatten(limit=300)

    return paginator

def paginator_users_tweets(authenticated_client, id):
    paginator = tweepy.Paginator(authenticated_client.get_users_tweets, id=id,
                                 max_results=100).flatten(limit=3200)
    return paginator

def create_df(data, *args):
    df = pd.DataFrame(data, columns=args)
    return df

def df_to_csv(df):
    df.to_csv('twitter.csv', encoding='utf-8', index=False)


def main():
    client = tweepy.Client(bearer_token=bearer)
    username = 'elonmusk'
    twitter_response = get_user_id(client, username)
    id = twitter_response.data.id
    paginator = paginator_users_tweets(client, id)
    data = []
    for item in paginator:
        data.append([item.id,item.text])
    df = create_df(data, 'Tweet ID', 'Tweet Text')
    df_to_csv(df)

if __name__ == "__main__":
    main()