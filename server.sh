#!/bin/bash
echo 'Server started'
pipe=~/cam.mjpg

#trap "rm -f $pipe" EXIT

# nc -l -p 2222 | mplayer -fps 31 -demuxer h264es -

echo 'Server IP Address:'
ifconfig | grep 'inet 19' | awk '{print $2}'

if [[ ! -p $pipe ]]; then
    echo 'Pipe file is not found, create one.'
    mkfifo $pipe
fi

nc -l -p 2222 > $pipe &
mplayer $pipe -fps 31 -demuxer h264es

