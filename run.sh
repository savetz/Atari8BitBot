docker build . -t ataribot
docker run --rm -e MASTODON_SERVER="https://mastodon.cloud/" \
-e CONSUMER_KEY= \
-e CONSUMER_SECRET= \
-e ACCESS_TOKEN= \
--device /dev/fuse --name Atari8bitBot --cap-add SYS_ADMIN  ataribot