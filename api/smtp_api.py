from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import subprocess

# PING 772109738@qq.com ([113.96.208.206]:25): 10299 bytes (SMTP DATA)
# seq=1, connect=28.45 ms, helo=95.32 ms, mailfrom=128.58 ms, rcptto=266.93 ms, datasent=822.85 ms, quit=854.83 ms
# seq=2, connect=26.57 ms, helo=74.71 ms, mailfrom=103.21 ms, rcptto=203.17 ms, datasent=602.16 ms, quit=627.99 ms
# seq=3, connect=19.08 ms, helo=75.52 ms, mailfrom=95.64 ms, rcptto=232.57 ms, datasent=837.42 ms, quit=860.39 ms
# seq=4, connect=28.06 ms, helo=63.57 ms, mailfrom=91.14 ms, rcptto=214.25 ms, datasent=631.49 ms, quit=657.59 ms
# seq=5, connect=22.51 ms, helo=88.27 ms, mailfrom=116.26 ms, rcptto=237.19 ms, datasent=778.03 ms, quit=806.08 ms
# seq=6, connect=22.09 ms, helo=61.23 ms, mailfrom=84.55 ms, rcptto=185.55 ms, datasent=586.65 ms, quit=606.61 ms
# seq=7, connect=35.06 ms, helo=100.57 ms, mailfrom=142.68 ms, rcptto=279.43 ms, datasent=753.96 ms, quit=796.96 ms
# seq=8, connect=36.33 ms, helo=96.83 ms, mailfrom=131.86 ms, rcptto=293.14 ms, datasent=745.12 ms, quit=781.45 ms
# seq=9, connect=20.42 ms, helo=83.33 ms, mailfrom=109.03 ms, rcptto=228.72 ms, datasent=628.41 ms, quit=649.47 ms
# seq=10, connect=27.75 ms, helo=73.11 ms, mailfrom=101.59 ms, rcptto=227.19 ms, datasent=704.76 ms, quit=731.87 ms

router = APIRouter(prefix='/api/smtp')

class Item(BaseModel):
    address: str
    server: Optional[str] = None
    port: Optional[str] = None

def execute_smtpping(item:Item):
    cmd = ['smtpping','--count','10']
    if(item.port != None):
        cmd.extend(['--port',item.port])
    cmd.extend([item.address])
    if(item.server != None):
        cmd.extend(['@'+item.server])
    print(cmd)
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
    res = proc.communicate()[0].decode('utf-8')
    return res

# fix dict[a][b]= c KeyError
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

def serialize_bench(bench):
    dict = Vividict()
    line = bench.splitlines() 
    dict['title'] = line[0]
    body = line[1:11]
    for index,seq in enumerate(body): # seq=10, connect=27.75 ms, helo=73.11 ms, mailfrom=101.59 ms, rcptto=227.19 ms, datasent=704.76 ms, quit=731.87 ms
        data = seq.split(', ') # seq=10
        for each in data:
            msg = each.split('=') # [seq,10]
            fil = filter(lambda ch: ch in '0123456789.', msg[1]) # remove ms
            msg[1] = ''.join(fil)
            dict[index][msg[0]] = msg[1]
    return dict

@router.post('')
def handle_smtp(item:Item):
    bench = execute_smtpping(item)
    res = serialize_bench(bench)
    return res
    