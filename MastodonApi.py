from mastodon import Mastodon
from bs4 import BeautifulSoup as bs
import logging
import re
import os

from types import SimpleNamespace

class MastodonApi:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    api = None

    def get_api(Self, client_id, client_secret, access_token, access_token_secret):
        Self.api=Mastodon(client_id, client_secret, access_token, os.getenv('MASTODON_SERVER') )
        return Self.api

    def media_upload(Self,filename):
        media = SimpleNamespace()
        mastodon_media = Self.api.media_post(filename,synchronous=True)
        media.media_id=mastodon_media.id
        return media

    def update_status(Self,text, media ,toot):
        id=toot.id
        status= Self.api.status_post(text,in_reply_to_id=id, media_ids=[media.media_id])
        return status

    def reply(Self, toot, text):
        msg=" "
        for line in text.split("\n"):
            if "ERROR"  in line or "error:" in line:
                msg=msg+line+"\n"

        Self.logger.info(f"MSG: {msg}")
        status = {}
        try:
            status = Self.api.status_post(msg,in_reply_to_id=toot.id)
        except:
            Self.logger.error(f"Unable to post message: {status}")

    def get_replies(Self, since_id):
        replies={}
        #result=api.search("#atari8bitbot", result_type="statuses",exclude_unreviewed=False, min_id=since_id)
        result=Self.api.timeline_hashtag("atari8bitbot", since_id=since_id)
        Self.logger.debug(f"result: {result}")
        for toot in result:
            #parse the message to extract entities
            message=Self.extract_entities(toot.content)
            status=SimpleNamespace()
            status.id = toot['id']
            status.entities={}
            if 'urls' in message.keys():
                if 'urls' not in status.entities.keys():
                    status.entities['urls']=[]
                status.entities['urls']=message['urls']
            status.user=SimpleNamespace()
            status.user.screen_name=toot.account.display_name
            status.user.name=toot.account.acct
            status.full_text=message['text'].strip()
            replies[status.id]=status
            Self.logger.debug(f"status: {status.id}")
        Self.logger.info(f"replies: {replies}")
        return replies.values()

    def extract_entities(Self,html_doc):
        message={}
        html_doc=re.sub(r'<br\s*/?>', '\n', html_doc)
        html_doc=re.sub(r'</p>', '\n', html_doc)
        html_doc=re.sub('<[^<]+?>', '', html_doc)
        html_doc=re.sub('#atari8bitbot\s?', '', html_doc, flags=re.IGNORECASE)
        soup = bs(html_doc, 'html.parser')
        message['text'] = soup.get_text(separator="\n")

        return message