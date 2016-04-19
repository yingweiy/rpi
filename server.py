import os
print('Server started ...')
os.system('nc -l 2222 | mplayer -fps 31 -demuxer h264es -')
