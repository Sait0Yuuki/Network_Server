import cv2
import time
import json
import pingparsing


myrtmp_addr = "rtmp://58.200.131.2:1935/livetv/hunantv"
cap = cv2.VideoCapture(myrtmp_addr)

dict = {}
dict['height'] = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
dict['width'] = cap.get(cv2.CAP_PROP_FRAME_WIDTH)


count = 0


while count < 6:
    t_end = time.time() + 10
    frame_count = 0
    while time.time() < t_end:
        ret, frame = cap.read()
        if ret is False:
            break
        frame_count = frame_count + 1
    dict[count] = frame_count/10
    count = count + 1

ping_parser = pingparsing.PingParsing()
transmitter = pingparsing.PingTransmitter()
transmitter.destination = '58.200.131.2'
transmitter.count = 6
result = transmitter.ping()
stats = ping_parser.parse(result)
dict['ping'] = stats.icmp_replies


print(dict)

cap.release()
cv2.destroyAllWindows()