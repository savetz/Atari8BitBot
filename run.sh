docker build . -t atari_bot
docker run --rm -e DRY_RUN=true \
-e CONSUMER_KEY= \
-e CONSUMER_SECRET= \
-e ACCESS_TOKEN= \
--device /dev/fuse --cap-add SYS_ADMIN --name Atari8bitBot ataribot