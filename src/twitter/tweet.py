'''
This file contains the logic for the twitter bot to tweet every 15 minutes
'''

import tweepy
import json
import requests
from utils import random_stat
from config import create_api
import time
import logging
import datetime

import os
import sentry_sdk
sentry_sdk.init(os.environ['SENTRY_DSN'])

logging.basicConfig(filename="bot.log",
                    filemode='a',
                    format='tweet.py | %(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%D - %H:%M:%S',
                    level=logging.DEBUG)

logging.info("Random Tweet bot running")
logger = logging.getLogger()

def random_tweet(api):
    stat = random_stat()
    while stat == None:
        stat = random_stat()
    
    fl = True
    while fl:
        try:
            api.update_status(status=stat)
            print(f"Random Tweet: {stat}")
            return
        except:
            stat = random_stat()
            while stat == None:
                stat = random_stat()
            continue

def main():
    api = create_api()
    random_tweet(api)

if __name__ == "__main__":
    # check if every 20 minutes
    fl = True
    minute = datetime.datetime.now().minute
    if (minute < 10) or (minute > 20 and minute < 30) or (minute > 40 and minute < 50):
        fl = False
    if fl:
        exit()
    else:
        main()





