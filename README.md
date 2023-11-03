# spotify-combine-playlists

Create dynamic combinations of your Spotify playlists! When you add or remove songs to your sub-playlists, the combined playlist automatically* updates.

This script will combine any number of your existing playlists and update those playlists when you add/remove songs from their sub-playlists.

Current version is a simple Python script that must be manually run to create or update combined playlists.

## Installation
This app uses the [Spotify Web API](https://developer.spotify.com/documentation/web-api) which requires the user to create an app on the [Spotify dashboard](https://developer.spotify.com/dashboard).

This app also uses [Spotipy](https://spotipy.readthedocs.io/en/latest/) to access the API, which requires [three environment variables](https://spotipy.readthedocs.io/en/latest/#quick-start) to be set where you are running this script. The values of these variables are given to you when you create your app in the Spotify dashboard. Simply create a `.env` file with the following:

```
SPOTIPY_CLIENT_ID=<id>
SPOTIPY_CLIENT_SECRET=<secret>
SPOTIPY_REDIRECT_URI=<url>
```

*I am working on a converting this script to a web app which would not require any installation*
