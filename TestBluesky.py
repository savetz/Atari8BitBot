
from atproto import Client
from atproto_client import models
from atproto import client_utils
import os
import datetime

def search_mentions(handle):
    results = []
    dummy_time=1633421325
    since_date= datetime.date.fromtimestamp(dummy_time)
    
    response = client.app.bsky.feed.search_posts(
            params = models.AppBskyFeedSearchPosts.Params(
                q=f"{handle}",
                since=f"{since_date.strftime('%Y-%m-%dT%H:%M:%SZ')}"
            )
    )
    results.extend(response.posts)
    return results


client = Client()
client.login('papa-robot.bsky.social', os.getenv('CONSUMER_SECRET'))
mentions = search_mentions("#atari8bitbot")
for post in mentions:
    print(post.record.text)
    print(post.author.handle)
    print(post.cid)

    video = open("examples/atari.mp4", 'rb')
    vid_data = video.read()
    this_parent = models.create_strong_ref(post)
    this_root = models.create_strong_ref(post)
    tb = client_utils.TextBuilder()
    tb.text("AtariBotTest got ")
    tb.mention(post.author.display_name, post.author.did)
    tb.text("'s post and replied, here is media")
    
    client.send_video(
        text=tb,
        reply_to=models.AppBskyFeedPost.ReplyRef(parent=this_parent, root=this_root),
        video=vid_data
    )


