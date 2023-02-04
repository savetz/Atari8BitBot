FROM python:stretch AS builder

WORKDIR /root
RUN wget -q --no-check-certificate  https://sourceforge.net/projects/atari8/files/franny/Franny-1.1.3/franny-1.1.3.tgz/download -O franny.tgz && tar -xzvf franny.tgz
RUN cd franny-1.1.3 && make franny
RUN ls -la /root/franny-1.1.3/
FROM  python:stretch AS base

ENV DEBIAN_FRONTEND=noninteractive
COPY nonfree.repo /etc/apt/sources.list.d/nonfree.list

#/home/atari8/bot/

RUN useradd atari -d /home/atari8
RUN apt update
RUN apt install -yq atari800 ffmpeg xdotool xvfb

RUN wget -q --no-check-certificate https://github.com/dmsc/tbxl-parser/releases/download/v10/basicParser-v10-0-gc06210e-linux64.zip && unzip basicParser-v10-0-gc06210e-linux64.zip && cp basicParser-v10-0-gc06210e/basicParser /usr/local/bin/ && chmod 755 /usr/local/bin/basicParser

COPY --chown=atari . /home/atari8
COPY --from=builder --chmod=755 /root/franny-1.1.3/franny /usr/local/bin/
WORKDIR /home/atari8
RUN pip3 install -r requirements.txt

USER atari
ENV DISPLAY=:99
ENV SDL_AUDIODRIVER=dummy
ENV PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/usr/local/sbin

RUN mkdir -p bot/working


CMD ./start.sh
