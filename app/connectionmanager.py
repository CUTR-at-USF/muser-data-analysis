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
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sqlalchemy import create_engine


# Connection Manager Architecture
class ConnectionManager:

    # The constructor extracts the credentials from the .env file
    def __init__(self):
        self.CLIENT_ID = os.environ.get('CLIENT_ID')
        self.CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
        self.CONNECTION_STRING = os.environ.get('CONNECTION_STRING')

    # Function to create a spotify connection object
    def spotify_connection(self):
        client_credentials_manager = SpotifyClientCredentials(self.CLIENT_ID, self.CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return sp

    # Function to create a sqlalchemy engine
    def database_connection(self):
        print(self.CONNECTION_STRING)
        engine = create_engine(self.CONNECTION_STRING, pool_pre_ping=True)
        return engine
