from django.shortcuts import render
from flask import Flask, request, redirect, g, render_template, session, url_for
from spotify_requests import spotify
import random
import sys
import requests
import lyricsgenius
import json

app = Flask(__name__)
app.secret_key = 'some key for session'

ans = ""
lives = 3

@app.route("/auth")
def auth():
    return redirect(spotify.AUTH_URL)


@app.route("/callback/")
def callback():
    auth_token = request.args['code']
    auth_header = spotify.authorize(auth_token)
    session['auth_header'] = auth_header

    return base()

def valid_token(resp):
    return resp is not None and not 'error' in resp

@app.route("/")
def index():
    if 'auth_header' in session:
        b = True
    else:
        b = False
    return render_template('index.html', login=b)

@app.route('/index')
def base():
    if 'auth_header' in session:
        auth_header = session['auth_header']
        # get profile data
        profile_data = spotify.get_users_profile(auth_header)
        # get user playlist data
        if valid_token(profile_data):
            return render_template("base.html",
                               user=profile_data)

    return render_template('profile.html')



def lyrics(song, artist):
    token = "0ex8GF9EFwR5_2cEv637XuJdMbK32fOgsjHoWBgyXoydD9B3n2LysgkQIPU12o3R"
    genius = lyricsgenius.Genius(token)

    lyrics = genius.search_song(song, artist).lyrics.split('\n')
    line = lyrics[random.randint(0, len(lyrics))].split(' ')

    while len(line) < 2 or line[0][0] == '[' or line[len(line)-1][0] == '(':
        line = lyrics[random.randint(0, len(lyrics))].split(' ')
    res = ["",""]
    shortenedline = ""
    for i in range(len(line)-1):
        shortenedline += line[i] + " "
    correct = line[len(line)-1]
    res[0] = shortenedline
    res[1] = correct
    global ans
    ans = correct
    return res

def check(guess):
    return [guess == ans, ans]
    

@app.route('/play')
def play():
    if 'auth_header' in session:
        auth_header = session['auth_header']
        # get profile data
        topdata = spotify.get_users_top(auth_header, 'tracks', 50)
        top = topdata['items']
        setOfThree = set()
        res = [1,2,3]
        while len(setOfThree) < 3:
            setOfThree.add(random.randint(1,49))
        lottery = list(setOfThree)
        res[0] = top[lottery[0]]
        res[1] = top[lottery[1]]
        res[2] = top[lottery[2]]
        profile_data = spotify.get_users_profile(auth_header)
        global lives
        global ans
        lives = 3
        ans = ""
        if valid_token(topdata):
            return render_template("play.html",
                               user=profile_data,
                               top = res)
    return render_template('play.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/play/<id>')
def track(id):
    if 'auth_header' in session:
        auth_header = session['auth_header']
        t = spotify.get_track(id, auth_header)
        v = lyrics(t['name'], t['artists'][0]['name'])
        l = range(len(v[1]))
    global lives
    return render_template('track.html', t=t, v=v, l=l, lives=lives)

@app.route('/result', methods=['POST'])
def result():
    guess = request.form['guess']

    if 'auth_header' in session:
        auth_header = session['auth_header']
        # get profile data
        topdata = spotify.get_users_top(auth_header, 'tracks', 50)
        top = topdata['items']
        setOfThree = set()
        res = [1,2,3]
        while len(setOfThree) < 3:
            setOfThree.add(random.randint(1,49))
        lottery = list(setOfThree)
        res[0] = top[lottery[0]]
        res[1] = top[lottery[1]]
        res[2] = top[lottery[2]]
        profile_data = spotify.get_users_profile(auth_header)
        checkRes = check(guess)
        global lives
        if not checkRes[0]:
            lives -= 1
        if lives == 0:
            return render_template("dead.html")
        if valid_token(topdata):
            return render_template("results.html",
                               user=profile_data,
                               top = res, truth=checkRes[0], answer=checkRes[1], lives=lives)

    return render_template('results.html', truth=checkRes[0], answer=checkRes[1], lives=lives)

@app.route('/profile')
def profile():
    if 'auth_header' in session:
        auth_header = session['auth_header']
        # get user playlist data
        playlist_data = spotify.get_users_playlists(auth_header)
        profile_data = spotify.get_users_profile(auth_header)
        # get user recently played tracks        
        if valid_token(profile_data):
            return render_template("profile.html",user=profile_data)

    return render_template('profile.html')

@app.route('/recentlyplayed')
def recentlyplayed():
    if 'auth_header' in session:
        auth_header = session['auth_header']
        # get profile data
        recently_played = spotify.get_users_recently_played(auth_header)
        profile_data = spotify.get_users_profile(auth_header)
        if valid_token(recently_played):
            return render_template("recently_played.html", user=profile_data, recently_played=recently_played["items"])

@app.route('/topartists')
def topartists():
    if 'auth_header' in session:
        auth_header = session['auth_header']
        # get profile data
        topdata = spotify.get_users_top(auth_header, 'artists', 5)
        top = topdata['items']
        profile_data = spotify.get_users_profile(auth_header)
        if valid_token(topdata):
            return render_template("top_artists.html", top=top, user=profile_data)

@app.route('/topsongs')
def topsongs():
    if 'auth_header' in session:
        auth_header = session['auth_header']
        # get profile data
        topdata = spotify.get_users_top(auth_header, 'tracks', 5)
        top = topdata['items']
        profile_data = spotify.get_users_profile(auth_header)
        if valid_token(topdata):
            return render_template("top_songs.html", top=top, user=profile_data)
    

if __name__ == "__main__":
    app.run(debug=True, port=spotify.PORT)