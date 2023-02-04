#!/bin/bash
echo "109805469211860904" > sinceFile.txt
nohup Xvfb :99 > /dev/null 2>&1 &
python3 AtariBotMastodon.py
