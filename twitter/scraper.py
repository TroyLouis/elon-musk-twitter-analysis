import tweepy
import os
import pandas as pd

# Authentication Token for Twitter API
BEARER = os.environ.get('bearer_token')

class Scraper():
    def __init__(self, client):
        self.client = client

    def get_user_id(self, username):
        '''
        :param username: String Twitter handle
        :return: String Twitter user ID
        '''
        response = self.client.get_user(username=username)
        return response.data.id


    def paginator_recent_tweets(self, *args, query, max_results, limit):
        '''
        :param query: String search query, for a full list: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
        :param args: String items returned in tweet object, for a full list: https://docs.tweepy.org/en/stable/expansions_and_fields.html#tweet-fields-parameter
        :param max_results: Integer between 10 & 100 for number of tweets returned
        :param limit: Integer max number of pages to go through
        :return: Paginator object
        '''
        paginator = tweepy.Paginator(self.client.search_recent_tweets, query=query,
                                     tweet_fields=args, max_results=max_results).flatten(limit=limit)

        return paginator

    def paginator_users_tweets(self, id, max_results, limit):
        '''
        :param id: Integer user ID
        :param max_results: Integer between 10-100
        :param limit: Max number of results
        :return: Paginator Object
        '''
        paginator = tweepy.Paginator(self.client.get_users_tweets, id=id,
                                     max_results=max_results).flatten(limit=limit)
        return paginator

    @staticmethod
    def unpack_paginator(paginator):
        '''
        :param paginator: Paginator Object
        :return: List
        '''
        tweets = []
        for tweet in paginator:
            tweets.append([tweet.id, tweet.text])
        return tweets

    @staticmethod
    def create_df(data, *args):
        '''
        :param data: List of lists to be turned into a dataframe
        :param args: Column names of df
        :return: Dataframe
        '''
        df = pd.DataFrame(data, columns=args)
        return df

    @staticmethod
    def df_to_csv(df):
        '''
        Takes in a dataframe and saves it as a csv in current file location
        '''
        df.to_csv('twitter.csv', encoding='utf-8', index=False)


def main():
    client = tweepy.Client(bearer_token=BEARER)
    scraper = Scraper(client)
    username = 'elonmusk'
    user_id = scraper.get_user_id(username)
    user_tweets = scraper.paginator_users_tweets(user_id,100,32)
    unpacked_paginator = scraper.unpack_paginator(user_tweets)
    df = scraper.create_df(unpacked_paginator, 'ID', 'Text')
    scraper.df_to_csv(df)

if __name__ == "__main__":
    main()