from dotenv import load_dotenv
import os

# Fast API Imports
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Spotify API Imports
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

# Google Gemini Imports
import google.generativeai as genai

# import wikipedia                                  https://pypi.org/project/wikipedia/
# wikipedia built in api (just testing for now)     https://api.wikimedia.org/wiki/Getting_started_with_Wikimedia_APIs
# import requests

load_dotenv()
GEMINI_KEY = os.getenv('GEMINI_API_KEY', "No value found for Gemini API key, please make sure to update your env file")
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', "No value found for Spotify Client ID, please make sure to update your env file")
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', "No value found for Spotify Client Secret, please make sure to update your env file")

# Fast API Configuration
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
base_url = "http://localhost:8000/artist/" # call fastapi dev main.py to run it

# Spotipy Configuration
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

# Gemini Configuration
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


### ROUTES

# Home page route
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"base_url": base_url}
    )

# Timeline for the artist route
@app.get("/artist/{url}")
def root(request: Request, url):
    album_results = spotify.artist_albums(url, album_type="album", limit=50)
    artist_results = spotify.artist(url)
    mergedDict = {**artist_results, **album_results}

    for album in mergedDict['items']:
        description = getGeminiAlbumDescription(mergedDict['name'], album['name'])
        album['ai_description'] = description

    return templates.TemplateResponse(
            request=request, name="timeline.html", context=mergedDict
    )

# Pure JSON data returned route
@app.get("/test/{url}")
async def root(request: Request, url):
    album_results = spotify.artist_albums(url, album_type="album", limit=50)
    artist_results = spotify.artist(url)
    mergedDict = {**artist_results, **album_results}
    for album in mergedDict['items']:
        description = getGeminiAlbumDescription(mergedDict['name'], album['name'])
        album['ai_description'] = description

    return mergedDict

# Route for simply testing Gemini response
@app.get("/genai-test/{name}/{album}")
async def root(request: Request, name, album):
    description = getGeminiAlbumDescription(name, album)
    return description

### FUNCTIONS

def getGeminiAlbumDescription(artistName: str, albumName: str):
    response = model.generate_content(f"In 100 words, describe the circumstances in which the album {albumName} by {artistName} was created and released. Do not mention the date or year the album was released, just focus on the artistic circumstances, critical response, and specific awards won if any. Feel free to talk about RIAA certifications if any accurate data is found on that. Don't say anything about the album cementing or solidifying the artist's status as anything.")
    return response.text

# From testing Wikipedia API for birthdays
# def getWikipedia(name: str):
#     url = 'https://api.wikimedia.org/feed/v1/wikipedia/en/featured/' + date
#     headers = {
#     'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
#     'User-Agent': 'YOUR_APP_NAME (YOUR_EMAIL_OR_CONTACT_PAGE)'
#     }
#     response = requests.get(url, headers=headers)
#     data = response.json()
#     print(data)
#     return data
