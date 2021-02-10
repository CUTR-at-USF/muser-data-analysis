'''
/*
 * Copyright (C) 2019-2020 University of South Florida
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 '''

# Import the dependencies
import pandas as pd
import time
import numpy as np
from AI.models import NLPModel


# Architecture of the Muser Data Builder
class MuserDataBuilder:

    # The constructor instantiates all the variables that would be used throughout the class
    def __init__(self, sp, conn):
        self.sp = sp
        self.conn = conn
        self.df = pd.read_csv('music-analysis.csv')

    # Function to add feature columns to the muser data
    # Replace the existing csv
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

        sleep_min = 2
        sleep_max = 5
        request_count = 0

        for idx in self.df.index:
            album = self.df.loc[idx, 'song_album_name']
            track = self.df.loc[idx, 'song_name']
            artist = self.df.loc[idx, 'song_artist_name']
            query = 'album:{} track:{} artist:{}'.format(album, track, artist)
            spotify_search = self.sp.search(query, limit=1, offset=0, type='track', market=None)

            request_count += 1
            if request_count % 5 == 0:
                time.sleep(np.random.uniform(sleep_min, sleep_max))

            if len(spotify_search['tracks']['items']) > 0:
                track_uri = spotify_search['tracks']['items'][0]['uri']
                audio_features = self.sp.audio_features(track_uri)[0]
                self.df.loc[idx, 'popularity'] = self.sp.track(track_uri)['popularity']
            else:
                target = album + ' ' + track + ' ' + artist
                nlp_model = NLPModel(self.sp, self.conn)
                audio_features = nlp_model.most_similar_doc(target)
                self.df.loc[idx, 'popularity'] = audio_features['popularity']

            self.df.loc[idx, 'acousticness'] = audio_features['acousticness']
            self.df.loc[idx, 'danceability'] = audio_features['danceability']
            self.df.loc[idx, 'energy'] = audio_features['energy']
            self.df.loc[idx, 'instrumentalness'] = audio_features['instrumentalness']
            self.df.loc[idx, 'liveness'] = audio_features['liveness']
            self.df.loc[idx, 'loudness'] = audio_features['loudness']
            self.df.loc[idx, 'speechiness'] = audio_features['speechiness']
            self.df.loc[idx, 'tempo'] = audio_features['tempo']
            self.df.loc[idx, 'valence'] = audio_features['valence']

        self.df.to_csv('music-analysis.csv')
