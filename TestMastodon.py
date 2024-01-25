#!/usr/bin/env python3

from mastodon import Mastodon
import logging
import re
import os

client_id=''
client_secret=''
access_token=''
api=Mastodon(client_id, client_secret, access_token, "https://oldbytes.space/" )
result=api.timeline_hashtag("atari8bitbot", since_id=111631532029675227)

for toot in result:
     print(toot['id'])
     print(toot['account']['username'])

print("----")

result=api.search("#atari8bitbot", result_type="statuses",exclude_unreviewed=False, min_id=111631532029675227)

for toot in result['statuses']:
    print(toot['id'])
    print(toot['account']['username'])