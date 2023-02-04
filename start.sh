#!/bin/bash
nohup Xvfb :99 > /dev/null 2>&1 &
python3 AtariBotMastodon.py
