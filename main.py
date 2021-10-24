import requests
import spotipy
from bs4 import BeautifulSoup
import os


CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

#
special_date = input('Which year do you want to travel to? Type the the date in this format YYYY-MM-DD:\n')
url = f'https://www.billboard.com/charts/hot-100/{special_date}'
response = requests.get(url)
music_page = response.text
special_year = special_date.split('-')[0]

sp = spotipy.Spotify(
    auth_manager=spotipy.SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt")
)

user_id = sp.current_user()['id']


soup = BeautifulSoup(music_page, 'html.parser')
songs = soup.find_all(name='span', class_='chart-element__information__song text--truncate color--primary')
songs_names = [song.getText() for song in songs]
artists = soup.find_all(name='span', class_ ='chart-element__information__artist text--truncate color--secondary')
artists_names = [artist.getText() for artist in artists]
song_artist = list(zip(songs_names, artists_names))

uri_list = []

for (song, artist) in song_artist:
    result = sp.search(q=(song, artist), type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        uri_list.append(uri)
    except IndexError:
        res = f"{song} - {artist} doesn't exist in Spotify. Skipped."


new_list = sp.user_playlist_create(user=user_id,
                                   name=f'{special_date} Billboard 100',
                                   public=False,
                                   collaborative=False,
                                   description='My playlist')


new_list_id = new_list['id']
sp.playlist_add_items(playlist_id=new_list_id, items=uri_list, position=None)
