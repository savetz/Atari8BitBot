
from atproto import Client, client_utils
from atproto_client import models
from bs4 import BeautifulSoup as bs
import logging
import re
import os

from types import SimpleNamespace

class BlueSkyApi:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    api = None

    def get_api(Self, client_id, client_secret, access_token, access_token_secret):
        c=Client()
        c.authenticate(client_id, client_secret)
        Self.api=c
        return Self.api

    def media_upload(Self,filename):
        video = open(filename, 'rb')
        vid_data = video.read()
        media=Self.api.send_video(video=vid_data)
        return media

    def update_status(Self,text, media ,id):
        status= Self.api.send_post(text=text,reply_to=id, embed=media)
        return status

    def reply(Self, post, text):

        msg=" "
        for line in text.split("\n"):
            if "ERROR"  in line or "error:" in line:
                msg=msg+line+"\n"

        Self.logger.info(f"MSG: {msg}")
        status = {}
        try:
            status = Self.api.send_post(text=msg,reply_to=post)
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
