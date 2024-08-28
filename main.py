from dotenv import load_dotenv
import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
GEMINI_KEY = os.getenv('GEMINI_API_KEY', "No value found for Gemini API key, please make sure to update your env file")
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', "No value found for Spotify Client ID, please make sure to update your env file")
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', "No value found for Spotify Client Secret, please make sure to update your env file")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
base_url = "http://localhost:8000/artist/" # call fastapi dev main.py to run it
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"base_url": base_url}
    )

# https://open.spotify.com/artist/6uIst176jhzooPMetg2rtH?si=ahyzpHfBQYq1hj1gzH_Z-Q
@app.get("/artist/{url}")
def root(request: Request, url):
    results = spotify.artist_albums(url, album_type="album")
    return templates.TemplateResponse(
            request=request, name="timeline.html", context=results
    )

@app.get("/test")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="timeline.html", context={}
    )

