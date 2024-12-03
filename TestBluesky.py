from blueskysocial import Client, Post, Video
c=Client()
c.authenticate("papa-robot.bsky.social", "4jN8t4ZZfKZUmR7f9fpE")
video = Video('path/to/video.mov')
post = Post('Video Post', with_attachments=video)
c.post(post)