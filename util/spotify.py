from base64 import b64encode

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import requests
import json
import os
import random

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET_ID = os.getenv("SPOTIFY_SECRET_ID")
BASE_URL = os.getenv("BASE_URL")

REDIRECT_URI = "{}/callback".format(BASE_URL)

# scope user_top_read,user-read-currently-playing,user-read-recently-played
SPOTIFY_URL_REFRESH_TOKEN = "https://accounts.spotify.com/api/token"

SPOTIFY_URL_NOW_PLAYING = (
    "https://api.spotify.com/v1/me/player/currently-playing?additional_types=track,episode"
)
SPOTIFY_URL_RECENTLY_PLAY = "https://api.spotify.com/v1/me/player/recently-played?limit=1"

SPOTIFY_URL_GENERATE_TOKEN = "https://accounts.spotify.com/api/token"

SPOTIFY_URL_USER_INFO = "https://api.spotify.com/v1/me"

SPOTIFY_URL_USER_TOP_READ = "https://api.spotify.com/v1/me/top/tracks"

SPOTIFY_URL_PLAYLIST_READ_PRIVATE = "https://api.spotify.com/v1/me/playlists"

SPOTIFY_URL_PLAYLIST_READ_COLLABORATIVE = "https://api.spotify.com/v1/users/8glrlrg13vyc6hu8tgw6sfvez/playlists"

SPOTIFY_URL_EPISODE = "https://api.spotify.com/v1/episodes/{id}"

def get_episode_by_id(access_token, episode_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = SPOTIFY_URL_EPISODE.format(id=episode_id)

    response = requests.get(url, headers=headers)
    
    if response.status_code == 404:
        return {"error": "Episode not found"}
    elif response.status_code == 401:
        return {"error": "Unauthorized - Invalid access token"}
    elif response.status_code != 200:
        return {"error": f"Failed to fetch episode. Status code: {response.status_code}"}

    return response.json()


def get_authorization():

    return b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_SECRET_ID}".encode()).decode("ascii")


def generate_token(authorization_code):

    data = {
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": authorization_code,
    }

    headers = {"Authorization": "Basic {}".format(get_authorization())}

    response = requests.post(SPOTIFY_URL_GENERATE_TOKEN, data=data, headers=headers)
    response_json = response.json()

    return response_json


def refresh_token(refresh_token):

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    headers = {"Authorization": "Basic {}".format(get_authorization())}

    response = requests.post(SPOTIFY_URL_REFRESH_TOKEN, data=data, headers=headers)
    response_json = response.json()

    return response_json


def get_user_profile(access_token):

    headers = {"Authorization": "Bearer {}".format(access_token)}

    response = requests.get(SPOTIFY_URL_USER_INFO, headers=headers)
    response_json = response.json()

    return response_json


def get_recently_play(access_token):

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(SPOTIFY_URL_RECENTLY_PLAY, headers=headers)

    if response.status_code == 204:
        return {}

    response_json = response.json()
    return response_json


def get_now_playing(access_token):

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(SPOTIFY_URL_NOW_PLAYING, headers=headers)

    if response.status_code == 204:
        return {}

    response_json = response.json()
    return response_json
    
def get_user_top_read(access_token):

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(SPOTIFY_URL_USER_TOP_READ, headers=headers)

    if response.status_code == 204:
        return {}

    response_json = response.json()
    return response_json

def get_playlist_read_private(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(SPOTIFY_URL_PLAYLIST_READ_PRIVATE, headers=headers)

    if response.status_code == 204:
        return {}

    response_json = response.json()
    return response_json

def get_playlist_read_collaborative(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(SPOTIFY_URL_PLAYLIST_READ_COLLABORATIVE, headers=headers)

    if response.status_code == 204:
        return {}

    response_json = response.json()
    return response_json