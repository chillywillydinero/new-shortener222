from fastapi import FastAPI, Request
from pydantic import BaseModel
import hashlib

app = FastAPI()
db = {}

class URLRequest(BaseModel):
    url: str

@app.post("/shorten")
async def shorten_url(data: URLRequest):
    hash_key = hashlib.md5(data.url.encode()).hexdigest()[:6]
    short_url = f"https://your-app.onrender.com/{hash_key}"
    db[hash_key] = data.url
    return {"short_url": short_url}

@app.get("/{short}")
async def redirect(short: str):
    url = db.get(short)
    if url:
        return {"redirect_to": url}
    return {"error": "URL not found"}
@app.get("/")
async def root():
    return {"message": "URL shortener is alive"}
