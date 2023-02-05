#Atari8BitBot by Kay Savetz 2020-2023. Mastodon: @savetz@oldbytes.space
#Mastodon conversion by @papa_robot@mastodon.cloud

import MastodonApi
import logging
import botConfig
import time
from shutil import copyfile
import os,sys
import subprocess
from datetime import datetime
from unidecode import unidecode
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for message in api.get_replies(since_id):
        new_since_id = max(message.id, new_since_id)

        logger.info(f"Toot from {message.user.name}")

        #remove all @ mentions, leaving just the BASIC code
        basiccode = re.sub('^(@.+?\s)+','',message.full_text, re.ASCII)

        basiccode = unidecode(basiccode)

        #unescape >, <, and &
        basiccode = basiccode.replace("&lt;", "<")
        basiccode = basiccode.replace("&gt;", ">")
        basiccode = basiccode.replace("&amp;", "&")
        #replace typogrphical quotes
        lead_double = u"\u201c"
        follow_double = u"\u201d"
        lead_single = u"\u2018"
        follow_single = u"\u2019"
        basiccode = basiccode.replace(lead_double, '"')
        basiccode = basiccode.replace(follow_double, '"')
        basiccode = basiccode.replace(lead_single, "'")
        basiccode = basiccode.replace(follow_single, "'")


#determine language:
        #look for start time command
        exp = "{\w*?B(\d\d?)\w*(?:}|\s)" # {B\d\d  B= Begin
        result = re.search(exp,basiccode)
        if result:
            starttime = int(result.group(1))
            logger.info(f" Requests start at {starttime} seconds")
        else:
            starttime = 3

        #look for length of time to record command
        exp = "{\w*?S(\d\d?)\w*(?:}|\s)" # {S\d\d  S= Seconds to record
        result=re.search(exp,basiccode)
        if result:
            recordtime = int(result.group(1))
            logger.info(f" Requests record for {recordtime} seconds")
        else:
            recordtime = 20
        if recordtime <1:
            recordtime=1

        language = 0 # default to BASIC

        exp = "{\w*?P\w*(?:}|\s)" #{P
        if re.search(exp,basiccode):
            language=1 #it's PILOT
            logger.info("it's PILOT")

        exp = "{\w*?L\w*(?:}|\s)" #{L
        if re.search(exp,basiccode):
            language=3 #it's LOGO
            logger.info("it's LOGO")
            if starttime==3:
                starttime=0

        exp = "{\w*?C\w*(?:}|\s)" #{C
        if re.search(exp,basiccode):
            language=4 #it's Action!
            logger.info("it's Action!")
            if starttime==3:
                starttime=0

        exp = "{\w*?M\w*(?:}|\s)" #{M
        if re.search(exp,basiccode):
            language=5 #MS BASIC
            logger.info("it's MS BASIC")

        exp = "{\w*?Q\w*(?:}|\s)" #{Q
        if re.search(exp,basiccode):
            language=6 #SuperPILOT
            logger.info("it's SuperPILOT")

        exp = "{\w*?A\w*(?:}|\s)" #{A
        if re.search(exp,basiccode):
            language=2 #it's Assembly
            logger.info("it's ASM")

            basiccode = "*=$3000\n" + basiccode
            lineNum=0
            newcode=""

            opcodes=['ADC','AND','ASL','BCC','BCS','BEQ','BIT','BMI','BNE','BPL','BRK','BVC','BVS','CLC','CLD','CLI','CLV','CMP','CPX','CPY','DEC','DEX','DEY','EOR','INC','INX','INY','JMP','JSR','LDA','LDX','LDY','LSR','NOP','ORA','PHA','PHP','PLA','PLP','ROL','ROR','RTI','RTS','SBC','SEC','SED','SEI','STA','STX','STY','TAX','TAY','TSX','TXA','TXS','TYA','*=']

            for line in basiccode.splitlines(True):
                #word = line.split()[0].upper()
                newcode = newcode + str(lineNum)+' '
                try:
                    if line.split()[0].upper() in opcodes or line[0]=="." or line[0]=="*":
                        newcode = newcode + " "
                except:
                    logger.info(f"could not dissect line {line}")
                newcode = newcode + line
                lineNum+=1
            basiccode=newcode

        #remove any { command
        #exp = "{\w*(?:}|\s)" #{anything till space or }
        exp = "{\w*(?:}\s*)" #{anything till } plus trailing whitespace
        basiccode = re.sub(exp,'',basiccode)

        #whitespace
        basiccode = basiccode.strip()

        #halt if string is empty
        if not basiccode:
            logger.info("!!! basiccode string is empty, SKIPPING")
            continue

        if language>0: #not BASIC
            basiccode=basiccode + "\n"
            basiccode=basiccode.replace("\n",chr(0x9B))
            outputFile = open('working/incomingBASIC.txt','w',encoding='latin')
        else:
            outputFile = open('working/incomingBASIC.txt','w')

        outputFile.write(basiccode)
        outputFile.close()

        if language==0: #BASIC
            #tokenize BASIC program
            result = os.system('basicParser -b -f -k -o working/AUTORUN.BAS working/incomingBASIC.txt')
            if result==256:
                logger.info("!!! PARSER FAILED, SKIPPING")
                continue


        if language==0: #BASIC
            logger.info("Making disk image, moving tokenized BASIC")
            copyfile('assets/TBXL.atr','working/disk.atr')
            result = os.system('/usr/local/franny/bin/franny -A working/disk.atr -i working/AUTORUN.BAS -o AUTORUN.BAS')

        elif language==1: #PILOT
            logger.info("Making disk image, moving text PILOT")
            copyfile('assets/pilot.atr','working/disk.atr')
            result = os.system('/usr/local/franny/bin/franny -A working/disk.atr -i working/incomingBASIC.txt -o MENU.SYS')

        elif language==2: #ASM
            logger.info("Making disk image, moving text ASM")
            copyfile('assets/asm.atr','working/disk.atr')
            result = os.system('/usr/local/franny/bin/franny -A working/disk.atr -i working/incomingBASIC.txt -o PROG')

        elif language==3: #Logo
            logger.info("Making disk image, moving text logo")
            copyfile('assets/dos2.atr','working/disk.atr')
            result = os.system('/usr/local/franny/bin/franny -A working/disk.atr -i working/incomingBASIC.txt -o PROG')

        elif language==4: #Action!
            logger.info("Making disk image, moving action code")
            copyfile('assets/action.atr','working/disk.atr')
            result = os.system('/usr/local/franny/bin/franny -A working/disk.atr -i working/incomingBASIC.txt -o BOT.ACT')

        elif language==5: #MS BASIC
            logger.info("Making disk image, moving MS BASIC code")
            copyfile('assets/MSBASIC.atr','working/disk.atr')
            result = os.system('/usr/local/franny/bin/franny -A working/disk.atr -i working/incomingBASIC.txt -o BOT.BAS')

        elif language==6: #SuperPILOT
            logger.info("Making disk image, moving SuperPILOT code")
            copyfile('assets/PILOTII.atr','working/disk.atr')
            result = os.system('/usr/local/franny/bin/franny -A working/disk.atr -i working/incomingBASIC.txt -o PROG')

        else:
            logger.error("Yikes! Langauge not valid")
            continue

        cmd = 'assets/atari800 -config atari800.cfg -o working/atari800_output.avi '

        if language==0: #BASIC
            cmd += f'-rec off'
        elif language==1: #PILOT
            cmd += f'-cart assets/PILOT.ROM -cart-type 1 -rec off'
        elif language==2: #ASM
            cmd += f'-cart assets/ASM.rom -cart-type 1 -rec off'
        elif language==3: #Logo
            cmd += "-cart assets/logo.ROM -cart-type 2 -rec off -step 2s -type 'LOAD \"D:PROG{ret}'"
        elif language==4: #Action!
            cmd += '-cart assets/action.ROM -cart-type 15 -rec off '
            cmd += " -step 60 -type '{shift}{ctrl}R' -step 5 -type 'D:BOT.ACT{ret}'"
            cmd += " -step 200 -type '{shift}{ctrl}M' -step 30 -type 'COMPILE{ret}'"
            cmd += " -step 400 -type 'RUN{ret}'"
        elif language==5: #MS BASIC
            cmd += "-cart assets/MSBASIC.bin -cart-type 2 -rec off -step 1s"
            cmd += " -type 'LOAD \"D:BOT.BAS{ret}' -step 1s -type 'RUN{ret}'"
        elif language==6: #SuperPILOT
            cmd += '-rec off -step 4s'
            cmd += " -type 'LOAD D:PROG{ret}'"
            cmd += " -step 1s -type 'RUN{ret}'"

        cmd += f' -step {starttime}s -rec on -step {recordtime}s working/disk.atr'

        logger.info("Firing up emulator")
        os.system(cmd)

        logger.info("Converting video")
        result = os.system('ffmpeg -loglevel warning -y -i working/atari800_output.avi -vcodec libx264 -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2,scale=1440:1080" -pix_fmt yuv420p -strict experimental -r 30 -t 2:20 -acodec aac -vb 1024k -minrate 1024k -maxrate 1024k -bufsize 1024k -ar 44100 -ac 2 working/OUTPUT_SMALL.mp4')
        #per https://gist.github.com/nikhan/26ddd9c4e99bbf209dd7#gistcomment-3232972

        logger.info("Uploading video")

        media = api.media_upload("working/OUTPUT_SMALL.mp4")

        logger.info(f"Media ID is {media.media_id}")

        time.sleep(5)

        logger.info(f"Posting message to @{message.user.name}")
        toottext = f"@{message.user.name} "
        post_result = api.update_status(toottext, media, message.id)

        logger.info("Done!")

    return new_since_id

def main():
    os.chdir('/home/atari8/bot/')

    api = botConfig.create_api_mastodon()

    now = datetime.now()
    logger.info("START TIME:")
    logger.info(now.strftime("%Y %m %d %H:%M:%S"))

    try:
        sinceFile = open('sinceFile.txt','r')
        since_id = sinceFile.read()
    except:
        sinceFile = open('sinceFile.txt','w')
        sinceFile.write("1")
        logger.info("created new sinceFile")
        since_id = 1

    sinceFile.close()
    since_id = int(since_id)
    logger.info(f"Starting since_id {since_id}")

    while True:
        didamessage=0
        new_since_id = check_mentions(api, since_id)

        if new_since_id != since_id:
            since_id = new_since_id
            logger.info(f"Since_id now {since_id}")

            sinceFile = open('sinceFile.txt','w')
            sinceFile.write(str(since_id))
            sinceFile.close()
            didamessage=1

        if didamessage==0:
            logger.info("Waiting...")
            time.sleep(120)

if __name__ == "__main__":
    main()
