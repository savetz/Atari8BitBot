
from atproto import Client
from atproto_client import models

def search_mentions(handle):
    results = []
    response = client.app.bsky.feed.search_posts(
            params = models.AppBskyFeedSearchPosts.Params(
                q=f"{handle}"
            )
    )
    results.extend(response.posts)
    return results


client = Client()
client.login('papa-robot.bsky.social', 'no tokens here')
mentions = search_mentions("#atari8bitbot")
for post in mentions:
    print(post.record.text)
