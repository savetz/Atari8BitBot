# Atari8BitBot
The code that runs the Atari 8-bit Twitter bot at https://twitter.com/Atari8BitBot

I'm sharing this so people can use this as a stepping stone to making their own, different bots.

Documentation for using the bot is at https://atari8bitbot.com

The main twitter posting code is based on what I learned from "The Reply to Mentions Bot" at https://realpython.com/twitter-bot-python-tweepy/#the-config-module

Dependencies. So many dependencies:
- A Twitter account, and API keys for it https://developer.twitter.com/en/products/twitter-api
- Tweepy. Specifically the fork that allows video uploads. https://github.com/tweepy/tweepy/pull/1414 They plan on folding that feature into the main program but as of this writing, haven't.
- atari800 emulator: https://github.com/atari800/atari800
- TBXL-Parser, for parsing Atari BASIC and TBXL programs: https://github.com/dmsc/tbxl-parser
- franny, an ATR disk image editor: http://atari8.sourceforge.net/franny.html and https://sourceforge.net/projects/atari8/files/franny/
- ffmpeg, for processing video files: https://ffmpeg.org
- and in the assets/ directory: ROM files: ATARIXL.ROM (the Atari XL operating system), logo.ROM (Atari Logo), PILOT.ROM (Atari PILOT), ASM.rom (Atari Assembler Editor), action.ROM (OSS Action!). These are not provided in this repository due to copyright.
- also in the assets/ directory: ATR disk images: action.atr (Action! Tooklit), PILOTII.atr (Atari Super PILOT), TBXL.atr (Turbo BASIC XL). These are not provided in this repository due to copyright.
- An X Virtual Frame Buffer running on display 99 (/usr/bin/Xvfb :99 -ac -screen 0 1024x768x24)
