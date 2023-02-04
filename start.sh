#!/bin/bash
echo "109808029753084484" > sinceFile.txt
nohup Xvfb :99 > /dev/null 2>&1 &
python3 AtariBotMastodon.py
