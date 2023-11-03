import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

FILE_NAME = "playlist.json"
SCOPE = "playlist-read-private playlist-modify-private playlist-modify-public"


def generate_combined_tracklist(sub_playlists):
    track_uris = []
    for uri in sub_playlists:
        tracks = sp.playlist(uri)['tracks']
        while True:
            track_uris += [track['track']['uri'] for track in tracks['items']]
            if not tracks['next']:
                break
            tracks = sp.next(tracks)
    return track_uris

def create_combined_playlist(sp):
    # List user's playlists
    all_playlists = sp.current_user_playlists()
    for i, playlist in enumerate(all_playlists['items']):
        print(f"[{i+1}] {playlist['name']}")

    # User selected sub-playlists
    sub_playlists = []
    print("Which of your playlists do you want to combine?")
    while True:
        try:
            user_input = input("Type the number of the playlist to add it or type 0 to finish: ")
            if user_input == '' or int(user_input) == 0:
                break
            elif int(user_input) < 0:
                raise IndexError
            print(f"Adding {all_playlists['items'][int(user_input)-1]['name']}")
            sub_playlists.append(all_playlists['items'][int(user_input)-1]['uri'])
        except ValueError:
            print("That is not a number.")
        except IndexError:
            print("That number does not correlate to a playlist. Take another look above.")

    # Generate combined tracklist
    track_uris = list(set(generate_combined_tracklist(sub_playlists)))

    # Create combined playlist
    user = sp.current_user()['id']
    playlist_name = input("Name of new playlist: ")

    new_playlist = sp.user_playlist_create(user, playlist_name, public=False)

    # Add tracks
    for i in range(0, len(track_uris), 100):
        # Spotify allows maximum of 100 tracks at a time
        sp.user_playlist_add_tracks(user, new_playlist['uri'], track_uris[i:i+100])

    try:
        with open(FILE_NAME, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {}
    with open(FILE_NAME, "w") as f:
        data[new_playlist['uri']] = {
            "playlists": sub_playlists,
        }
        f.write(json.dumps(data, indent=4))

def update_playlists(sp):
    print("Updating playlists...")
    try:
        with open(FILE_NAME, "r") as f:
            data = {}
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                print(f"No data found in {FILE_NAME}")
        with open(FILE_NAME, "w") as f:
            for uri in data:
                # Compare playlist with sub-playlists
                sub_playlists = data[uri]["playlists"]
                new_tracks = generate_combined_tracklist(sub_playlists)
                current_tracks = generate_combined_tracklist([uri])
                remove_tracks = set(current_tracks) - set(new_tracks)
                add_tracks = set(new_tracks) - set(current_tracks)
                if remove_tracks:
                    print(f"Removing {len(remove_tracks)} from the playlist")
                    print(sp.playlist_remove_all_occurrences_of_items(uri, remove_tracks))
                if add_tracks:
                    print(f"Adding {len(add_tracks)} to the playlist")
                    sp.playlist_add_items(uri, add_tracks)
                
                data[uri] = {
                        "playlists": sub_playlists,
                    }
            f.write(json.dumps(data, indent=4))

    except FileNotFoundError:
        print(f"{FILE_NAME} not found, no playlist to update!")


if __name__ == "__main__":
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
    update_playlists(sp)
    while True:
        user_input = input("Would you like to make a new combined playlist? (y/n): ")
        if user_input.lower() == "n":
            break
        if user_input.lower() == "y":
            create_combined_playlist(sp)
            break
