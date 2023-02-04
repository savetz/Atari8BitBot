FROM python:stretch

ENV DEBIAN_FRONTEND=noninteractive
COPY nonfree.repo /etc/apt/sources.list.d/nonfree.list

#/home/atari8/bot/

RUN useradd atari -d /home/atari8
RUN apt update
RUN apt install -yq atari800 ffmpeg xdotool xvfb

RUN wget -q --no-check-certificate https://github.com/dmsc/tbxl-parser/releases/download/v10/basicParser-v10-0-gc06210e-linux64.zip && unzip basicParser-v10-0-gc06210e-linux64.zip && cp basicParser-v10-0-gc06210e/basicParser /usr/local/bin/

COPY --chown=atari . /home/atari8
WORKDIR /home/atari8
RUN pip3 install -r requirements.txt

USER atari
ENV DISPLAY=:99
ENV SDL_AUDIODRIVER=dummy
ENV PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/usr/local/sbin

RUN mkdir -p bot/working


CMD ./start.sh
