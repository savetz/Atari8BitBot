#!/bin/bash
#uncomment for testing or in docker, this should be already existing in bm

#echo "109808029753084484" > sinceFile.txt
#nohup Xvfb :99 > /dev/null 2>&1 &

#select backend twitter/mastodon

#export BACKEND="mastodon"
#export MASTODON_SERVER="https://oldbytes.space/"

#Add credentials here

#export CONSUMER_KEY=""
#export CONSUMER_SECRET=""
#export ACCESS_TOKEN=""

#need this one for twitter
#export ACCESS_TOKEN_SECRET=""

python3 AtariBot.py
