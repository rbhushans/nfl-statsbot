'''
This file contains the logic for the twitter bot to reply to mentions
'''

import tweepy
import os
from config import create_api
import logging
from dotenv import load_dotenv
import numpy as np
import random
from urllib3.exceptions import ProtocolError, ReadTimeoutError
import sys
sys.path.append('src/utils')
from parsers import tweet_parser
from stats import player_stat, team_stat
from load_constants import categories, years

load_dotenv(override=True)
users = np.genfromtxt("data/users.txt", dtype='str').tolist()
self_id = "1373049656318431232"
api = create_api()

logging.basicConfig(filename="logs/bot.log",
                    filemode='a',
                    format='reply.py | %(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%D - %H:%M:%S',
                    level=logging.DEBUG)

logging.info("Reply bot running")
logger = logging.getLogger()

class MyStreamListener(tweepy.Stream):
    def on_status(self, tweet):
        if tweet.user.id == self_id:
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
        p, t = tweet_parser(tweet.text)

        #find a name/team
        r = random.randint(0, len(categories)-1)
        r_category = categories[r]
        r = random.randint(0, len(years)-1)
        r_year = years[r]
        
        if p == [] and t == []:
            print("Empty")
            return
        elif p == []:
            msg = team_stat(t[0], True, r_year, r_category)
            while msg == None:
                r = random.randint(0, len(categories)-1)
                r_category = categories[r]
                r = random.randint(0, len(years)-1)
                r_year = years[r]
                msg = team_stat(t[0], True, r_year, r_category)
            print("Reply Parameters:", t[0], r_year, r_category)
        else:
            msg = player_stat(p[0], r_year, r_category)
            while msg == None or "did not play" in msg:
                r = random.randint(0, len(categories)-1)
                r_category = categories[r]
                r = random.randint(0, len(years)-1)
                r_year = years[r]
                msg = player_stat(p[0], r_year, r_category)
            print("Reply Parameters:", p[0], r_year, r_category)
        
        print(f"Replying to {tweet.user.name} with {msg}")
        
        try:
            api.update_status(
                status=msg,
                in_reply_to_status_id=tweet.id,
                auto_populate_reply_metadata=True
            )
            print("Tweet sent successfully")
        except Exception as e:
            print("Error with Tweet:", e)
            return

    def on_error(self, status):
        print("Error detected")

def main():
    consumer_key = os.getenv("API_KEY")
    consumer_secret = os.getenv("API_KEY_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    stream = MyStreamListener(consumer_key, consumer_secret, access_token, access_token_secret)
    print(users)
    stream.filter(follow=users, stall_warnings=True)

if __name__ == "__main__":
    main()

