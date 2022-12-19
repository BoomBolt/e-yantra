import cv2
cap=cv2.VideoCapture(0)
fourcc=cv2.VideoWriter_fourcc(*'XVID')
out=cv2.VideoWriter('demo.avi' ,fourcc,20.0,(640,480))
ret,frame=cap.read()
while(not ret):
    continue
while(ret):
    ret,frame=cap.read();
    out.write(frame)
    cv2.imshow('frame',frame)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()