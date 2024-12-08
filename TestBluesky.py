
from atproto import Client
from atproto_client import models
from atproto import client_utils
import os
import datetime
from zoneinfo import ZoneInfo

TEST_VIDEO=False

def search_mentions(handle):
    results = []
    test_time=1733592061831+100
    since_date= datetime.datetime.fromtimestamp(test_time/1000, tz=ZoneInfo("UTC"))
    
    print(since_date.isoformat(timespec='milliseconds')+"Z")

    response = client.app.bsky.feed.search_posts(
            params = models.AppBskyFeedSearchPosts.Params(
                q=f"{handle}",
                since=since_date.isoformat(timespec='milliseconds')
            )
    )
    results.extend(response.posts)
    return results


client = Client()
client.login('atari8bitbot.bsky.social', os.getenv('CONSUMER_SECRET'))
mentions = search_mentions("#atari8bitbot")
for post in mentions:
    
    print("----")
    print(post.cid)
    print(post.record.text)
    print(post.record.created_at)
    ts=datetime.datetime.fromisoformat(post.record.created_at)
    print(int(ts.timestamp()*1000))

    if TEST_VIDEO:
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


