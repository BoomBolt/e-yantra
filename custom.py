import cv2 as cv2
import numpy as np

#saving feed from external usb web cam

video = cv2.VideoCapture(1)

frame_width = int(video.get(3))
frame_height = int(video.get(4))
   
size = (frame_width, frame_height)

#result = cv2.VideoWriter('arena_video_1.avi', cv2.VideoWriter_fourcc(*'DIVX'),30, (int(video.get(3)),int(video.get(4))))


while video.isOpened():
    ret, frame = video.read()
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUYV)
    #result.write(frame)
    cv2.imshow("frame", frame)
    
    
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
# Release video
video.release()
#result.release()
cv2.destroyAllWindows()
