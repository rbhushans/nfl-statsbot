from dotenv import load_dotenv
import os
import tweepy
import logging

#load env
load_dotenv(override=True)
logging.basicConfig(filename="bot.log",
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

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        print("ERROR: Did not configure API")
        logger.error("Error creating API", exc_info=True)
        raise e
    print("API Created")
    logger.info("API Created")
    return api