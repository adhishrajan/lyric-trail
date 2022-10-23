# lyric-trail

## How to run:
As it has not been officially 'released', Lyric Trail is best run by cloning the repo, and running `python app.py` in the command line.

## Inspiration

The Lyric Trail was inspired by the fusion between the past and present. In the modern space, Spotify is one of the most popular apps people use on a daily basis. This is combined with Oregon Trail, an extremely popular game that was released more than 50 years ago, to create an experience that is simultaneously retro and contemporary. We thought it was a fun way to present a modern idea with a vintage flair.

## What it does

The Lyric Trail is a full-stack web application that entertains users with a fun ‘finish-the-lyric’ guessing game curated personally from your favorite music. 

## How we built it

When developing this application, we wanted a nostalgic and retro-themed user interface that excites users. One of the tools that we used to create the front end of the application was Adobe XD, where we were able to make UI mockups and plan out the classic look of the game.

The backend architecture of the application consisted of a Python Flask REST API. We utilized the Spotify Web API, whose endpoints return JSON metadata about music artists, albums, and tracks, directly from the Spotify Data Catalogue. Our front-end architecture consisted of an HTML/CSS/JS application. To retrieve song lyrics, we used an open-source project called LyricsGenius, which required some use of the Genius API.

## Challenges we ran into

We originally had issues with creating a strong and nostalgic UI, but we overcame this challenge through the use of Adobe XD.

We faced many challenges in utilizing the APIs, especially because of the OAuth tokens. We also faced some challenges in dealing with authorization code flow and its user authentication issues. We were able to overcome these challenges with time and perseverance, through which we learned a lot more about full-stack web development.

## Accomplishments that we're proud of

Despite the many setbacks, we're very proud that we were able to create a minimal yet powerful entertaining application that will attract users. Though there is always room to improve, Lyric Trail is a fully functioning game as it is. Furthermore, with only two members, dividing the work and getting to every feature we hoped to implement was difficult, but we are proud that we overcame these challenges.

## What we learned

We cannot stress how much of a learning opportunity our project was. We improved our front-end skills significantly through this project, practicing using Flask and JavaScript to dynamically alter pages. We also learned how to integrate the Spotify Web API into our web application in order to display information about users, music, artists, albums, and tracks. This integration included learning about parsing through JSON metadata, OAuth services, and authorization code flow. Finally, we learned much more about using Flask to create web applications, as well as the extent of its functionality.

## What's next for The Lyric Trail

We are planning on adding real-time audio playback in correlation with the lyrics alongside album art pixelation to align with the retro style of the game. We are also considering implementing multiplayer options in which you can compete with your friends. 

