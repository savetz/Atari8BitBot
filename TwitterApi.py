import tweepy
import logging
import re
import os

from types import SimpleNamespace
from bs4 import BeautifulSoup

class TwitterApi:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    api = None

    def get_api(Self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True,
            wait_on_rate_limit_notify=True)
        try:
            api.verify_credentials()
        except Exception as e:
            Self.logger.error("Error creating API", exc_info=True)
            raise e
        Self.logger.info("API created")
        return api

    def media_upload(Self,filename):
        media = Self.api.media_upload(filename)
        return media;

    def update_status(Self,text, media ,id):
        status = Self.api.update_status(auto_populate_reply_metadata=False, status=text, media_ids=[media.media_id], in_reply_to_status_id=id)
        return status

    def reply(Self, tweet, text):
        msg=" "
        for line in text.split("\n"):
            if "ERROR"  in line or "error:" in line:
                msg=msg+line+"\n"

        Self.logger.info(f"MSG: {msg}")
        status = {}
        try:
            status = Self.update_status(msg,in_reply_to_id=tweet.id)
        except:
            Self.logger.error(f"Unable to post message: {status}")


    def get_replies(Self, since_id):
        return tweepy.Cursor(Self.api.mentions_timeline, since_id=since_id, tweet_mode='extended').items()

