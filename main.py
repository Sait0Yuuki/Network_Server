from fastapi import FastAPI
import uvicorn

app = FastAPI()

from api import dns_api, ftp_api, http_api, smtp_api

app.include_router(http_api.router)
app.include_router(dns_api.router)
app.include_router(smtp_api.router)
app.include_router(ftp_api.router)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=5000)