from MastodonApi import MastodonApi
import logging
import os

logger = logging.getLogger()

def create_api():
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

