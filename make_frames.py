import cv2
import os


vidcap = cv2.VideoCapture(os.path.join("data",'north_trim','north_trim.mp4'))
success,image = vidcap.read()
count = 0
while success:
  count += 1
  cv2.imwrite(os.path.join(".","data","north_trim","img1",f"{str(count).zfill(6)}.jpg"), image)     # save frame as JPEG
  success,image = vidcap.read()
  print('Read a new frame: ', success)
