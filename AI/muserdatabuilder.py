import pandas as pd
import os
from AI.models import NLPModel

os.chdir(r'C:\Users\sriva\Desktop\edu.usf.sas.pal.muser\SpotifyDataExtractor')

class MuserDataBuilder:
    def __init__(self, sp, conn):
        self.sp = sp
        self.conn = conn
        self.df = pd.read_csv('music-analysis.csv')

    def build_muser_data(self):
        self.df['acousticness'] = '' * self.df.shape[0]
        self.df['danceability'] = '' * self.df.shape[0]
        self.df['energy'] = '' * self.df.shape[0]
        self.df['instrumentalness'] = '' * self.df.shape[0]
        self.df['liveness'] = '' * self.df.shape[0]
        self.df['loudness'] = '' * self.df.shape[0]
        self.df['speechiness'] = '' * self.df.shape[0]
        self.df['tempo'] = '' * self.df.shape[0]
        self.df['valence'] = '' * self.df.shape[0]
        self.df['popularity'] = '' * self.df.shape[0]
        for idx in self.df.index:
            album = self.df.loc[idx, 'song_album_name']
            track = self.df.loc[idx, 'song_name']
            artist = self.df.loc[idx, 'song_artist_name']
            query = 'album:{} track:{} artist:{}'.format(album, track, artist)
            spotify_search = self.sp.search(query, limit=1, offset=0, type='track', market=None)
            if len(spotify_search['tracks']['items']) > 0:
                track_uri = spotify_search['tracks']['items'][0]['uri']
                audio_features = self.sp.audio_features(track_uri)[0]

                self.df.loc[idx, 'acousticness'] = audio_features['acousticness']
                self.df.loc[idx, 'danceability'] = audio_features['danceability']
                self.df.loc[idx, 'energy'] = audio_features['energy']
                self.df.loc[idx, 'instrumentalness'] = audio_features['instrumentalness']
                self.df.loc[idx, 'liveness'] = audio_features['liveness']
                self.df.loc[idx, 'loudness'] = audio_features['loudness']
                self.df.loc[idx, 'speechiness'] = audio_features['speechiness']
                self.df.loc[idx, 'tempo'] = audio_features['tempo']
                self.df.loc[idx, 'valence'] = audio_features['valence']
                self.df.loc[idx, 'popularity'] = self.sp.track(track_uri)['popularity']
            else:
                target = album + ' '+ track + ' ' + artist
                nlp_model = NLPModel(self.sp, self.conn)
                audio_features = nlp_model.most_similar_doc(target)
                self.df.loc[idx, 'acousticness'] = audio_features['acousticness']
                self.df.loc[idx, 'danceability'] = audio_features['danceability']
                self.df.loc[idx, 'energy'] = audio_features['energy']
                self.df.loc[idx, 'instrumentalness'] = audio_features['instrumentalness']
                self.df.loc[idx, 'liveness'] = audio_features['liveness']
                self.df.loc[idx, 'loudness'] = audio_features['loudness']
                self.df.loc[idx, 'speechiness'] = audio_features['speechiness']
                self.df.loc[idx, 'tempo'] = audio_features['tempo']
                self.df.loc[idx, 'valence'] = audio_features['valence']
                self.df.loc[idx, 'popularity'] = audio_features['popularity']

        self.df.to_csv('music-analysis.csv')


