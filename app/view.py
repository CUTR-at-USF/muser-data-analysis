from app import app
from flask import Flask, request, render_template
#app = Flask(__name__)

import os
from app.connectionmanager import ConnectionManager
from AI.spotifydataextractor import SpotifyDataExtractor
from AI.ETL import ETL
from AI.models import NLPModel
from AI.muserdatabuilder import MuserDataBuilder

os.chdir(r'C:\Users\sriva\Desktop\edu.usf.sas.pal.muser\SpotifyDataExtractor')

connection_manager = ConnectionManager()
sp = connection_manager.spotify_connection()
engine = connection_manager.database_connection()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/extract',methods=['POST','GET'])
def extract():
    try:
        input_query = request.form
        print(input_query)
        genre = input_query['genre']
        genre_data = sp.search(genre)
        artist_list = {}

        for i in range(len(genre_data['tracks']['items'])):
            for j in range(len(genre_data['tracks']['items'][i]['artists'])):
                artist_list[genre_data['tracks']['items'][i]['artists'][j]['uri']] = genre_data['tracks']['items'][i]['artists'][j]['name']
        print('{} uris found for the {} genre'.format(len(artist_list), genre))
        for uri, name in artist_list.items():
            extractor = SpotifyDataExtractor(sp, uri, name, engine)
            extractor.build_dataframe()
        print('Data extraction completed for the genre {}.'.format(genre))
        etl = ETL(engine)
        etl.build_final_table()
        print('Final table ready for analysis')
        return render_template('index.html', msg='Extraction completed' )
    except Exception as e:
        print(e)

@app.route('/build_model',methods=['POST','GET'])
def build_model():
    try:
        nlp = NLPModel(sp, engine)
        nlp.build_model()
        return render_template('index.html', msg='Model built successfully')
    except Exception() as e:
        print(e)

@app.route('/build_muser_data',methods=['POST','GET'])
def build_muser_data():
    try:
        builder = MuserDataBuilder(sp, engine)
        builder.build_muser_data()
        return render_template('index.html', msg='Muser data built successfully')
    except Exception() as e:
        print(e)

if __name__ == '__main__':
    app.run(port=80)
