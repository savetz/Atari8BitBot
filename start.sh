#!/bin/bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

nohup Xvfb :99 > /dev/null 2>&1 &
python3 AtariBot.py
