from dotenv import load_dotenv
import os
import tweepy
import logging

#load env
load_dotenv(override=True)
logging.basicConfig(filename="logs/bot.log",
                    filemode='a',
                    format='config.py | %(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%D - %H:%M:%S',
                    level=logging.DEBUG)

logging.info("Random Tweet bot running")
logger = logging.getLogger()

def create_api():
    consumer_key = os.getenv("API_KEY")
    consumer_secret = os.getenv("API_KEY_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )

    api = tweepy.API(auth)
    print("API Created")
    logger.info("API Created")
    return api