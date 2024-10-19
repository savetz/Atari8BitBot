#!/usr/bin/env python3

from mastodon import Mastodon
from bs4 import BeautifulSoup as bs
import logging
import re
import os


def extract_entities(html_doc):
     message={}
     html_doc=re.sub(r'<br\s*/?>', '\n', html_doc)
     html_doc=re.sub(r'</p>', '\n', html_doc)
     html_doc=re.sub(r'<[^<]+?>', '', html_doc)
     html_doc=re.sub(r'#atari8bitbot\s?', '', html_doc, flags=re.IGNORECASE)
     soup = bs(html_doc, 'html.parser')
     message['text'] = soup.get_text(separator="\n")
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