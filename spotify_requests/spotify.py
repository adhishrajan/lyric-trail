import base64
import json
import requests
import sys
import urllib.request, urllib.error
import urllib.parse as urllibparse

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = "v1"
SPOTIFY_API_URL = f"{SPOTIFY_API_BASE_URL}/{API_VERSION}"

# endpoints
SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL.format('api/token')

# Client keys
CLIENT = json.load(open('conf.json', 'r+'))
CLIENT_ID = CLIENT['id']
CLIENT_SECRET = CLIENT['secret']
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8081
REDIRECT_URI = "{}:{}/callback/".format(CLIENT_SIDE_URL, PORT)
SCOPE = "user-library-read user-read-recently-played user-top-read"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

URL_ARGS = "&".join(["{}={}".format(key, urllibparse.quote(val))
                    for key, val in list(auth_query_parameters.items())])

AUTH_URL = f"{SPOTIFY_AUTH_URL}/?{URL_ARGS}"

def authorize(auth_token):
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload,
                                 headers=headers)
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    return auth_header


GET_ARTIST_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'artists')

def get_artist(artist_id):
    url = "{}/{id}".format(GET_ARTIST_ENDPOINT, id=artist_id)
    resp = requests.get(url)
    return resp.json()

USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')
USER_PLAYLISTS_ENDPOINT = "{}/{}".format(USER_PROFILE_ENDPOINT, 'playlists')
USER_TOP_ARTISTS_AND_TRACKS_ENDPOINT = "{}/{}".format(
    USER_PROFILE_ENDPOINT, 'top')  
USER_RECENTLY_PLAYED_ENDPOINT = "{}/{}/{}".format(USER_PROFILE_ENDPOINT,
                                                  'player', 'recently-played')
BROWSE_FEATURED_PLAYLISTS = "{}/{}/{}".format(SPOTIFY_API_URL, 'browse',
                                              'featured-playlists')

def get_users_profile(auth_header):
    url = USER_PROFILE_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()

def get_users_playlists(auth_header):
    url = USER_PLAYLISTS_ENDPOINT
    myparams = {'limit': 5}
    resp = requests.get(url, headers=auth_header, params=myparams)
    return resp.json()

def get_users_top(auth_header, t, limit):
    if t not in ['artists', 'tracks']:
        print('invalid type')
        return None
    myParams = {'limit': limit}
    url = "{}/{type}".format(USER_TOP_ARTISTS_AND_TRACKS_ENDPOINT, type=t)
    resp = requests.get(url, headers=auth_header, params=myParams)
    return resp.json()

def get_users_recently_played(auth_header):
    url = USER_RECENTLY_PLAYED_ENDPOINT
    myparams = {'limit': 5}
    resp = requests.get(url, headers=auth_header, params=myparams)
    return resp.json()

GET_USER_ENDPOINT = '{}/{}'.format(SPOTIFY_API_URL, 'users')


def get_user_profile(user_id):
    url = "{}/{id}".format(GET_USER_ENDPOINT, id=user_id)
    resp = requests.get(url)
    return resp.json()

GET_TRACK_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'tracks')  # /<id>

def get_track(track_id, auth_header):
    url = f"{GET_TRACK_ENDPOINT}/{track_id}"
    resp = requests.get(url, headers=auth_header)
    return resp.json()