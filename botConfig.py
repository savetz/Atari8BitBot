

import MastodonApi
import TwitterApi

import logging
import os

logger = logging.getLogger()

def create_api_twitter():
    consumer_key =  os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    t = TwitterApi()
    try:
        api = t.get_api(consumer_key, consumer_secret, access_token, access_token_secret)
    except Exception as e:
        logger.error("Error creating internal API", exc_info=True)
        raise e
    logger.info("API created")
    return t

def create_api_mastodon():
    consumer_key =  os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = ""

    m = MastodonApi()
    try:
        api = m.get_api(consumer_key, consumer_secret, access_token, access_token_secret)
    except Exception as e:
        logger.error("Error creating internal API", exc_info=True)
        raise e
    logger.info("API created")
    return m