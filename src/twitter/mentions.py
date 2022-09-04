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
import os

import os
import sentry_sdk
sentry_sdk.init(os.environ['SENTRY_DSN'])

logging.basicConfig(filename="bot.log",
                    filemode='a',
                    format='mentions.py | %(asctime)s | %(levelname)s | %(message)s',
                    datefmt='%D - %H:%M:%S',
                    level=logging.DEBUG)

logging.info("Mentions bot running")
logger = logging.getLogger()

def check_mentions(api, since_id):
    new_since_id = since_id
    # print(since_id)
    
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        if not tweet.favorited:
            try:
                tweet.favorite()
            except Exception as e:
                print("Error on fav", exc_info=True)
                continue
        else:
            # print("skipping")
            return
        try:
            new_since_id = max(tweet.id, new_since_id)
        except:
            print("TWEET ID:", tweet.id)
            print("NEW SINCE ID:", new_since_id)
            new_since_id = tweet.id
        print(f"{tweet.user.name}:{tweet.text}")
        msg = ""

        play, team, year, cat, positions = utils.mention_parser(tweet.text)
        print("Parameters: ", str(play), str(team), str(year), str(cat), str(positions))
        err = False
        if year == [None]:
            msg = "NFLStatsbot now requires a year to be provided - please include a year when requesting statistics"
        if play == [None] and team == [None] and cat == [None]:
            post_error(api, tweet)
        elif team == [None] and cat == [None]:
            msg = "That request was invalid! Make sure to use a valid category: https://github.com/rbhushans/nfl-statsbot/blob/master/data/cat_format.csv"
        elif team == [None] and play == [None]:
            msg = "I don't recognize that player or team! Make sure that you are spelling the name correctly."
        else:
            i = 0
            for p in play:
                if p == None:
                    break
                for c in cat:
                    if err:
                        err = False
                        break
                    if c is not None and "_allowed" in c:
                        c = c.replace("_allowed", "")
                    for y in year:
                        try:
                            stat = utils.player_stat(p, y, c, positions[i])
                            i += 1
                        except:
                            post_error(api, tweet)
                            return new_since_id
                        if stat == None:
                            continue
                        m =  stat + "\n"
                        if len(msg) + len(m) > 280:
                            break
                        msg += m
                        if "did not play in the NFL" in stat or "rookies from the 2020 NFL season" in stat:
                            err = True
                            break
            for t in team:
                if t == None:
                    break
                for c in cat:
                    if c is not None and "_allowed" in c:
                        off = False
                        c = c.replace("_allowed", "")
                    else:
                        off = True
                    for y in year:    
                        try:                    
                            stat = utils.team_stat(t, off, y, c)
                        except:
                            post_error(api, tweet)
                            return new_since_id
                        if stat == None:
                            continue
                        m =  stat + "\n"
                        if len(msg) + len(m) > 280:
                            break
                        msg += m

        print(f"Answering to {tweet.user.name} with {msg}")
        post_reply(api, msg, tweet)
    os.environ["SINCE_ID"] = str(new_since_id)
    return new_since_id

def post_reply(api, msg, tweet):
    try:
        api.update_status(
            status=msg,
            in_reply_to_status_id=tweet.id,
            auto_populate_reply_metadata=True
        )
    except Exception as e:
        print("Error replying:", e)
        print("\tmsg =",msg)

def post_error(api, tweet):
    stat = utils.random_stat()
    while stat == None:
        stat = utils.random_stat()
    msg = "That request was invalid! Check my pinned post for details on how to call the bot. Common issues include not @/ing the bot or not separating the parameters by commas. Here's a random stat: " + stat
    post_reply(api, msg, tweet)

def main():
    api = create_api()
    since_id = int(os.getenv("SINCE_ID"))
    while True:
        try:
            since_id = check_mentions(api, since_id)
            # print("Waiting...")
            time.sleep(10)
        except Exception as e:
            print("Error replying:", e)
            continue

if __name__ == "__main__":
    main()





