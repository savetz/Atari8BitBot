#!/usr/bin/env python3

from mastodon import Mastodon
import logging
import re
import os


def extract_entities(html_doc):
     message={}
     html_doc=re.sub('<br />', '\n', html_doc)
     html_doc=re.sub('<[^<]+?>', '', html_doc)
     message['text']=re.sub('#atari8bitbot\s?', '', html_doc, flags=re.IGNORECASE)
     return message

client_id=''
client_secret=''
access_token=''
api=Mastodon(client_id, client_secret, access_token, "https://oldbytes.space/" )

result=api.timeline_hashtag("atari8bitbot", since_id=113303702916012370)
for toot in result:
    print(toot.content)
    print("----")
    print(extract_entities(toot.content))
    #print(toot['account']['username'])