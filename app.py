from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import RedirectResponse
import string
import random

app = FastAPI()

url_map = {}

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(chars) for _ in range(length))
        if code not in url_map:
            return code

@app.get("/")
async def root():
    return {"message": "URL shortener is alive"}

@app.post("/shorten")
async def shorten_url(long_url: str = Form(...)):
    if not long_url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL")
    short_code = generate_short_code()
    url_map[short_code] = long_url
    short_url = f"https://new-shortener222.onrender.com/{short_code}"
    return {"short_url": short_url}

@app.get("/{short_code}")
async def redirect_url(short_code: str):
    long_url = url_map.get(short_code)
    if long_url:
        return RedirectResponse(long_url)
    raise HTTPException(status_code=404, detail="URL not found")
