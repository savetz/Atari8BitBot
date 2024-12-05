
from atproto import Client, client_utils
from atproto_client import models
from bs4 import BeautifulSoup as bs
import logging
import re
import os
import datetime

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
        #just validate the videa file as reply does it
       
        return filename

    def update_status(Self,text, media ,id):
        #this_parent = models.create_strong_ref(post)
        #this_root = models.create_strong_ref(post)

        video = open(media, 'rb')
        vid_data = video.read()
    
        status= Self.api.send_video(
            text        =   text,
            reply_to    =   id,
            video       =   vid_data
            )
        return status

    def reply(Self, post, text):
        msg=" "
        for line in text.split("\n"):
            if "ERROR"  in line or "error:" in line:
                msg=msg+line+"\n"

        Self.logger.info(f"MSG: {msg}")

        this_parent = models.create_strong_ref(post)
        this_root = models.create_strong_ref(post)

        status = {}
        try:
            status = Self.api.send_post(
                text=msg,
                reply_to=models.AppBskyFeedPost.ReplyRef(parent=this_parent, root=this_root))
        except:
            Self.logger.error(f"Unable to post message: {status}")

    def get_replies(Self, since_id):
        replies={}
        result = []
        since_date= datetime.date.fromtimestamp(since_id)
        response = Self.api.t.app.bsky.feed.search_posts(
            params = models.AppBskyFeedSearchPosts.Params(
                q="#atari8bitbot",
                since=f"{since_date.strftime('%Y-%m-%dT%H:%M:%SZ')}"
            )
        )
        result.extend(response.posts)

        Self.logger.debug(f"result: {result}")
        for post in result:
            #parse the message to extract entities
            message=Self.extract_entities(post.record.text)
            status=SimpleNamespace()
            status.id = post.record.cid
            status.entities={}
            if 'urls' in message.keys():
                if 'urls' not in status.entities.keys():
                    status.entities['urls']=[]
                status.entities['urls']=message['urls']
            status.user=SimpleNamespace()
            status.user.screen_name=post.author.display_name
            status.user.name=post.author.handle
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