#!/bin/bash
#uncomment for testing, this shouls be already running

echo "109814700946549490" > sinceFile.txt
nohup Xvfb :99 > /dev/null 2>&1 &

python3 AtariBotMastodon.py
