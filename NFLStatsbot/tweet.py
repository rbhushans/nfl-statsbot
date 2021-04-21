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

import os
import sentry_sdk
sentry_sdk.init(os.environ['SENTRY_DSN'])
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

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

@sched.scheduled_job('interval', minutes=20)
def main():
    api = create_api()
    while True:
        logger.info("Tweeting random tweet!")
        random_tweet(api)

sched.start()




