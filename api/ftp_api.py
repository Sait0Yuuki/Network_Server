from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import subprocess
import json
import csv

router = APIRouter(prefix='/api/ftp')

class Item(BaseModel):
    host: str
    user: str
    password: str
    method: int
    dir: str # 1: login 2: upload 3:download

# ftpbench -h 159.75.123.97 -u uftp -p axziOblYTpz5Yh663KaA login
def execute_ftpbench(item:Item):
    cmd = ['ftpbench']
    cmd.extend(['-h',item.host])
    cmd.extend(['-u',item.user])
    cmd.extend(['-p',item.password])
    cmd.extend(['--maxrun=1'])
    cmd.extend(['--csv','src/ftpdata.csv']) 
    if(item.method == 0):
        cmd.extend(['login'])
    elif(item.method == 1):
        cmd.extend(['upload',item.dir])
    else:
        cmd.extend(['download',item.dir])
    print(cmd)
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE)
    return proc

def serialize_bench(proc):
    proc.communicate()[0].decode('utf-8')
    with open('src/ftpdata.csv') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    res = json.loads(json.dumps(rows))
    return res

@router.post('')
def handle_ftp(item:Item):
    proc = execute_ftpbench(item)
    res = serialize_bench(proc)
    return res