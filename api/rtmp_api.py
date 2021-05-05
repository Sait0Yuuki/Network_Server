from fastapi import APIRouter
from pydantic import BaseModel
import subprocess
import json
import cv2
import time
import pingparsing

router = APIRouter(prefix='/api/rtmp')

class Item(BaseModel):
    host: str
    dir: str
    port: str

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

def ping_bench(dict,host):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = host
    transmitter.count = 6
    result = transmitter.ping()
    stats = ping_parser.parse(result)
    stats.icmp_replies
    dict['ping'] = stats.icmp_replies


def frame_bench(dict,addr):
    cap = cv2.VideoCapture(addr)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    dict['resolution'] = str(height) + '*' +  str(width)
    # test 60s
    count = 0
    while count < 6:
        t_end = time.time() + 10
        frame_count = 0
        while time.time() < t_end:
            ret, frame = cap.read()
            if ret is False:
                break
            frame_count = frame_count + 1
        dict['fps'][count] = frame_count/10
        count = count + 1

# rtmp://58.200.131.2:1935/livetv/hunantv
def execute_rtmpbench(item:Item):
    addr = 'rtmp://'+ item.host + ':' + item.port + item.dir
    print(addr)
    dict = Vividict()
    frame_bench(dict,addr)
    ping_bench(dict,item.host)
    return dict

@router.post('')
def handle_ftp(item:Item):
    res = execute_rtmpbench(item)
    return res