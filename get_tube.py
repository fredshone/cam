from pytube import YouTube
import os

while True:
    try:
        YouTube('https://www.youtube.com/watch?v=4vHh-aDeUco').streams.first().download(os.path.join('.','sample','sample1.avi'))
        print('done')
        break
    except:
        print('try again')
