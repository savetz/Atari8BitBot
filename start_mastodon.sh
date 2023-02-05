#!/bin/bash
#uncomment for testing, this shouls be already running

#echo "109808029753084484" > sinceFile.txt
#nohup Xvfb :99 > /dev/null 2>&1 &

export MASTODON_SERVER="https://oldbytes.space/"
export CONSUMER_KEY=""
export CONSUMER_SECRET=""
export ACCESS_TOKEN=""

python3 AtariBotMastodon.py
