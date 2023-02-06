#!/bin/bash
#uncomment for testing or in docker, this should be already existing in bm

#echo "109808029753084484" > sinceFile.txt
#nohup Xvfb :99 > /dev/null 2>&1 &

#Add credentials here

#export MASTODON_SERVER="https://oldbytes.space/"
#export CONSUMER_KEY=""
#export CONSUMER_SECRET=""
#export ACCESS_TOKEN=""

python3 AtariBotMastodon.py
