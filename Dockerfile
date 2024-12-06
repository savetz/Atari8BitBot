FROM python:3.12-bullseye AS builder
RUN apt update
RUN apt install -yq peg gawk

WORKDIR /root
RUN wget -q --no-check-certificate  https://sourceforge.net/projects/atari8/files/franny/Franny-1.1.3/franny-1.1.3.tgz/download -O franny.tgz && tar -xzvf franny.tgz
RUN cd franny-1.1.3 && make franny
RUN ls -la /root/franny-1.1.3/

RUN wget -q --no-check-certificate https://github.com/dmsc/tbxl-parser/archive/refs/tags/v10.tar.gz -O tbxl-parser-10.tar.gz && tar -zxf tbxl-parser-10.tar.gz && cd tbxl-parser-10 && make CROSS= EXT= CFLAGS='-Wall -O2 -flto -DNDEBUG'

RUN git clone https://github.com/robmcmullen/atari800.git && cd atari800 && git checkout headless && ./autogen.sh && ./configure --target=headless && make && make install

FROM python:3.12-bullseye AS base

ENV DEBIAN_FRONTEND=noninteractive
COPY nonfree.repo /etc/apt/sources.list.d/nonfree.list
#/home/atari8/bot/

RUN useradd atari -d /home/atari8
RUN apt update
RUN apt install -yq ffmpeg xdotool xvfb libc6 libsdl1.2debian
RUN mkdir -p /home/atari8/bot && chown atari /home/atari8/bot
RUN mkdir -p /usr/local/franny/bin/

COPY --chown=atari . /home/atari8/bot

COPY --from=builder --chmod=755 /root/franny-1.1.3/franny /usr/local/franny/bin/
COPY --from=builder --chmod=755 /root/tbxl-parser-10/build/basicParser /usr/local/bin/
COPY --from=builder --chmod=755 /usr/local/bin/atari800 /home/atari8/bot/assets/

WORKDIR /home/atari8/bot
RUN pip3 install -r requirements.txt

USER atari
ENV DISPLAY=:99
ENV PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/usr/local/sbin

RUN mkdir -p working

CMD ["./start.sh"]
