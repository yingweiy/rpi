#!/bin/bash
echo 'Server started'
nc -l 2222 | mplayer -fps 31 -demuxer h264es -
