from fastapi import APIRouter
from pydantic import BaseModel
import requests

router = APIRouter(prefix='/api/dns')

class Item(BaseModel):
    host: str
    qtype: str

@router.post('')
def handle_dns(item:Item):
    url = 'https://myssl.com/api/v1/tools/dns_query'
    payload = {'qtype': item.qtype, 'host': item.host, 'qmode': -1}
    res = requests.get(url,params=payload)
    return res.json()