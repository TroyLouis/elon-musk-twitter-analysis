import tweepy
import os

bearer_token = os.environ.get('BEARER')

client = tweepy.Client(bearer_token)

tweets = client.get_users_tweets(id="44196397")

def main():
    print(tweets.meta['next_token'])


if __name__ == "__main__":
    main()