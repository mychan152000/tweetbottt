#!/usr/bin/env python
# sneeze-translator/sneeze-translator.py

from Processor import Processor
import os
import json
from dotenv import load_dotenv
import logging
import discord
import tweepy
from tweepy.streaming import StreamListener
from time import strftime
from datetime import datetime
from queue import Queue
from threading import Thread
import urllib3.exceptions

from config import create_api

load_dotenv()
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
WH_URL = os.environ['WH_URL']
USERS = [
    '1321879104317132800',
    '1108236843466711043',
    '1430575943433691154',
    '1276939850885656576',
    '1345372835254992896',
    '1041912206583984130',
    '1325769100803534849',
    '1041915108069261313',
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class TweetStreamListener(StreamListener):
    def __init__(self, api, q=Queue()):
        super().__init__()
        #self.api = api
        #self.me = api.me()
        self.color = 0
        num_worker_threads = 4
        self.q = q
        for i in range(num_worker_threads):
            t = Thread(target=self._on_status)
            t.daemon = True
            t.start()

    def _on_status(self):
        while True:
            data = self.q.get()._json
            tweet_id = data["id"]
            date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"[{date_time}] Processing tweet id {tweet_id}")

            if data["user"]["id_str"] in USERS:
                if data["user"]["id_str"] == '1321879104317132800':
                    self.color = 5991156
                elif data["user"]["id_str"] == '1108236843466711043':
                    self.color = 5991156
                elif data["user"]["id_str"] == '1276939850885656576':
                    self.color = 255212216
                elif data["user"]["id_str"] == '1345372835254992896':
                    self.color = 255212216
                elif data["user"]["id_str"] == '1041912206583984130':
                    self.color = 18650111
                elif data["user"]["id_str"] == '1325769100803534849':
                    self.color = 191182200
                elif data["user"]["id_str"] == '1041915108069261313':
                    self.color = 191182200
                elif data["user"]["id_str"] == '1430575943433691154':
                    self.color = 14177041
                else:
                    self.color = 1127128

                date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"[{date_time}] Match")
                p = Processor(status_tweet=data)
                p.create_embed(self.color)
                p.attach_field()
                p.attach_media()
                p.attach_translation()
                p.send_message(WH_URL)

            else:
                date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"[{date_time}] No match")

            self.q.task_done()

    def on_status(self, tweet):
        self.q.put(tweet)

    def on_error(self, status):
        logger.error(status)


if __name__ == "__main__":
    api = create_api()
    tweets_listener = TweetStreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(follow=USERS, is_async=True, stall_warnings=True)
