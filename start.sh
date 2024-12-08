#!/bin/bash
#uncomment for testing or in docker, this should be already existing in bm

#echo "109910943006026066" > sinceFile.txt
nohup Xvfb :99 2>&1 &
python3 AtariBot.py
