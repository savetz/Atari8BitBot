FROM python:bullseye AS builder

RUN apt update
RUN apt install -yq peg gawk

WORKDIR /root
RUN wget -q --no-check-certificate  https://sourceforge.net/projects/atari8/files/franny/Franny-1.1.3/franny-1.1.3.tgz/download -O franny.tgz && tar -xzvf franny.tgz
RUN cd franny-1.1.3 && make franny
RUN ls -la /root/franny-1.1.3/

RUN wget -q --no-check-certificate https://github.com/dmsc/tbxl-parser/archive/refs/tags/v10.tar.gz -O tbxl-parser-10.tar.gz && tar -zxf tbxl-parser-10.tar.gz && cd tbxl-parser-10 && make CROSS= EXT= CFLAGS='-Wall -O2 -flto -DNDEBUG'


FROM  python:bullseye AS base

ENV DEBIAN_FRONTEND=noninteractive
COPY nonfree.repo /etc/apt/sources.list.d/nonfree.list
#/home/atari8/bot/

RUN useradd atari -d /home/atari8
RUN apt update
RUN apt install -yq ffmpeg xdotool xvfb libc6 libsdl1.2debian
RUN wget -q --no-check-certificate https://github.com/atari800/atari800/releases/download/ATARI800_5_0_0/atari800_5.0.0_amd64.deb && dpkg -i atari800_5.0.0_amd64.deb
RUN mkdir -p /home/atari8/bot && chown atari /home/atari8/bot
RUN mkdir -p /usr/local/franny/bin/

COPY --chown=atari . /home/atari8/bot
COPY --from=builder --chmod=755 /root/franny-1.1.3/franny /usr/local/franny/bin/
COPY --from=builder --chmod=755 /root/tbxl-parser-10/build/basicParser /usr/local/bin/
WORKDIR /home/atari8/bot
RUN pip3 install -r requirements.txt

USER atari
ENV DISPLAY=:99
ENV SDL_AUDIODRIVER=dummy
ENV PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/usr/local/sbin

RUN mkdir -p working


CMD ./start.sh
