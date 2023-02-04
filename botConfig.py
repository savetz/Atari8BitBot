import MastodonApi
import logging

logger = logging.getLogger()

def create_api():
    consumer_key = "????"
    consumer_secret = "????"
    access_token = "????"
    access_token_secret = "????"

    m = MastodonApi()
    try:
        api = m.get_api(consumer_key, consumer_secret, access_token, access_token_secret)
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

