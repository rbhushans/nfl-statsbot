'''
This file contains the logic for the twitter bot to reply to mentions
'''

import tweepy
import json
import requests
import utils
from config import create_api
import time
import logging
import numpy as np
import random
from urllib3.exceptions import ProtocolError, ReadTimeoutError

users = np.genfromtxt("../../data/users.txt", dtype='str').tolist()

logging.basicConfig(filename="bot.log",
                    filemode='a',
                    format='reply.py | %(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%D - %H:%M:%S',
                    level=logging.DEBUG)

logging.info("Reply bot running")
logger = logging.getLogger()

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        if tweet.user.id == self.me.id:
            return
        if hasattr(tweet, 'retweeted_status'):
            return
        if str(tweet.user.id) not in users:
            return
        ttt = tweet.text.lower()
        checks_bad = ["pray", "terrible", "die", "condolence", "death", "dead", "kill", "acl", "injur", "dead", "out for the season", "rip", "passed away", "pass away"]
        for c in checks_bad:
            if c in ttt:
                return

        print(f"{tweet.user.name}:{tweet.text}")
        p, t = utils.tweet_parser(tweet.text)

        #find a name/team
        r = random.randint(0, len(utils.categories)-1)
        r_category = utils.categories[r]
        r = random.randint(0, len(utils.years)-1)
        r_year = utils.years[r]
        
        if p == [] and t == []:
            print("Empty")
            return
        elif p == []:
            msg = utils.team_stat(t[0], True, r_year, r_category)
            while msg == None:
                r = random.randint(0, len(utils.categories)-1)
                r_category = utils.categories[r]
                r = random.randint(0, len(utils.years)-1)
                r_year = utils.years[r]
                msg = utils.team_stat(t[0], True, r_year, r_category)
            print("Reply Parameters: " + t[0] + r_year + r_category)
        else:
            msg = utils.player_stat(p[0], r_year, r_category)
            while msg == None or "did not play" in msg:
                r = random.randint(0, len(utils.categories)-1)
                r_category = utils.categories[r]
                r = random.randint(0, len(utils.years)-1)
                r_year = utils.years[r]
                msg = utils.player_stat(p[0], r_year, r_category)
            print("Reply Parameters: " + p[0] + r_year + r_category)
        
        print(f"Replying to {tweet.user.name} with {msg}")
        
        try:
            self.api.update_status(
                status=msg,
                in_reply_to_status_id=tweet.id,
                auto_populate_reply_metadata=True
            )
        except:
            return

    def on_error(self, status):
        print("Error detected")

def main():
    api = create_api()
    tweets_listener = MyStreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    print(users)
    stream.filter(follow=users, stall_warnings=True)

    
if __name__ == "__main__":
    main()

