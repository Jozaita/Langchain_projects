from dotenv import load_dotenv
import requests
import tweepy
import os
load_dotenv()

twitter_client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_SECRET_KEY"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"] )


def scrape_user_tweets(username,num_tweets=5,mock=True):
    """Scrapes a twitter user original tweets and returns them as a list of dictionaries. Each dictionary contains three fields: time_posted, text and url"""
    tweet_list = []

    if mock: 
        EDEN_TWITTER_LIST = "https://gist.githubusercontent.com/emarco177/9d4fdd52dc432c72937c6e383dd1c7cc/raw/1675c4b1595ec0ddd8208544a4f915769465ed6a/eden-marco-tweets.json"
        tweets = requests.get(EDEN_TWITTER_LIST,timeout=10).json()

    else:
        user_id = twitter_client.get_user(username=username).data.id
        tweets = twitter_client.get_users_tweets(id=user_id,max_results=num_tweets,exclude=["retweets","replies"])

    for tweet in tweets:
        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet["id"]}"
        tweet_list.append(tweet_dict)

    return tweet_list

if __name__ == "__main__":
    tweets = scrape_user_tweets(username="sanchezcastejon")
    print(tweets)