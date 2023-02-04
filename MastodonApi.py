from mastodon import Mastodon
import logging
import re

from types import SimpleNamespace
from bs4 import BeautifulSoup

class MastodonApi:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    def get_api(Self, client_id, client_secret, access_token, access_token_secret):
        api=Mastodon(client_id, client_secret, access_token, "https://mastodon.cloud/" )
        return api

    def media_upload(Self, api,filename):
        media = SimpleNamespace()
        mastodon_media = api.media_post(filename,synchronous=True)
        media.media_id=mastodon_media.id
        return media

    def update_status(Self, api,text,id, media):
        status= api.status_post(text,in_reply_to_id=id, media_ids=[media.media_id])
        return status

    def reply(Self,api, toot, text):

        msg=" "
        for line in text.split("\n"):
            if "ERROR"  in line or "error:" in line:
                msg=msg+line+"\n"

        Self.logger.info(f"MSG: {msg}")
        status = {}
        try:
            status = api.status_post(msg,in_reply_to_id=toot.id)
        except:
            Self.logger.error(f"Unable to post message: {status}")

    def get_replies(Self, api, since_id):
        replies={}
        #result=api.search("#zxspectrumbot", result_type="statuses",exclude_unreviewed=False, min_id=since_id)
        result=api.timeline_hashtag("zxspectrumbot", since_id=since_id)
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
            status.full_text=message['text']
            replies[status.id]=status
            Self.logger.debug(f"status: {status.id}")
        Self.logger.info(f"replies: {replies}")
        return replies.values()

    def extract_entities(Self,html_doc):
        message={}
        soup = BeautifulSoup(html_doc, 'html.parser')
        #Remove mention and hashtag
        mentions=soup.find_all("a", class_="mention")
        for m in mentions:
            m.decompose()
        all_links=soup.find_all('a',attrs={'target':'_blank'} )
        if all_links:
            message['urls']=[]
        for link in all_links:
            message['urls'].append( {'expanded_url': link.get('href')} )
        expr = re.compile("#zspectrumbot", re.IGNORECASE)
        message['text']=expr.sub("",soup.get_text(separator="\n"))
        return message