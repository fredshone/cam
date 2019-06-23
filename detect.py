import cv2
import os


vidcap = cv2.VideoCapture(os.path.join('sample','file_example_AVI_480_750kB.avi'))
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite(os.path.join(".","sample","frames",f"frame{count}.jpg"), image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1
