#!/usr/bin/env python
import requests
import time
import os

spotify_oauth_token = os.environ['SPOTIFY_OAUTH_TOKEN']
twitter_bearer_token = os.environ['TWITTER_BEARER_TOKEN']


lastSongPlayed = ""

def postTweet(songName, artistName, songURL):
    data = f"{songName}\n{artistName}\n {songURL}"
    twitter_request = requests.post("https://api.twitter.com/2/tweets", headers={"Authorization": "Bearer " + twitter_bearer_token}, json={"text": data})
    if twitter_request.status_code == 201:
        print(f"Posted new Song to Twitter! {data}")
    else:
        print(f"Error while posting new Song to Twitter! {twitter_request.status_code}")

def getSpotifyArtists(rawArtists):
    artists = []
    for artist in rawArtists:
        artists.append(artist['name'])
    return artists


if __name__ == "__main__":
    while (True):
        spotify_request = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers={"Authorization": "Bearer " + spotify_oauth_token})
        # Checks to verify if the request was successful
        if spotify_request.status_code == 200:
            spotify_json = spotify_request.json()
            # Checks to see if there is a song playing
            if spotify_json["is_playing"] and spotify_json["item"]["id"] != lastSongPlayed:
                lastSongPlayed = spotify_json["item"]["id"]
                # Prints the song name and artist
                postTweet(spotify_json["item"]["name"], ', '.join(getSpotifyArtists(spotify_json["item"]["artists"])), spotify_json["item"]["external_urls"]["spotify"])
            else:
                # Prints that there is no song playing
                print("No song playing, or same song playing")
        else:
            print("Spotify API Error: " + str(spotify_request.status_code))
        time.sleep(60)

