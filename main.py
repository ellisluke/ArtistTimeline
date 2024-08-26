from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

load_dotenv()
GEMINI_KEY = os.getenv('GEMINI_API_KEY', "No value found, please make sure to update your env file")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
base_url = "http://localhost:8000/" # call fastapi dev main.py to run it

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"base_url": base_url}
    )

@app.get("/{artistName}")
async def artistSearch(artistName):
    return {"Looking for": artistName}