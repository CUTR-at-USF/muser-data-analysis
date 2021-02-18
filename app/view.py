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
from app import app
from flask import request, render_template, send_file

from app.connectionmanager import ConnectionManager
from AI.spotifydataextractor import SpotifyDataExtractor
from AI.ETL import ETL
from AI.models import NLPModel
from AI.muserdatabuilder import MuserDataBuilder
from io import BytesIO
import pandas as pd

# Creates an object of the ConnectionManager class
# To create connections to spotify and sql server database
from reports.report import MuserReport
import os
from os.path import join, dirname, realpath

connection_manager = ConnectionManager()
sp = connection_manager.spotify_connection()
engine = connection_manager.database_connection()
# Upload folder
DOWNLOAD_FOLDER = 'reports/downloads/'
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

UPLOAD_FOLDER = 'reports/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return render_template('index.html')


# Function to call the spotifydataharvester and ETL classes for harvesting spotify data
@app.route('/extract', methods=['POST', 'GET'])
def extract():
    try:
        input_query = request.form
        genre = input_query['genre']
        genre_data = sp.search(genre)
        artist_list = {}

        for i in range(len(genre_data['tracks']['items'])):
            for j in range(len(genre_data['tracks']['items'][i]['artists'])):
                artist_list[genre_data['tracks']['items'][i]['artists'][j]['uri']] = \
                    genre_data['tracks']['items'][i]['artists'][j]['name']
        print('{} uris found for the {} genre'.format(len(artist_list), genre))
        for uri, name in artist_list.items():
            extractor = SpotifyDataExtractor(sp, uri, name, engine)
            extractor.build_database()
        print('Data extraction completed for the genre {}.'.format(genre))
        etl = ETL(engine)
        etl.build_final_table()
        print('Final table ready for analysis')
        return render_template('index.html', msg='Extraction completed')
    except Exception as e:
        print(e)


# Function to call the NLPModel class and build a doc2vec model trained on the harvested data stored in sql database
@app.route('/build_model', methods=['POST', 'GET'])
def build_model():
    try:
        nlp = NLPModel(sp, engine)
        nlp.build_model()
        return render_template('index.html', msg='Model built successfully')
    except Exception() as e:
        print(e)


# Function to build the muser data from the Firebase database
# for additional information extracted from spotify or # the sql database
@app.route('/build_muser_data', methods=['POST', 'GET'])
def build_muser_data():
    try:
        builder = MuserDataBuilder(sp, engine)
        builder.build_muser_data()
        return render_template('index.html', msg='Muser data built successfully')
    except Exception() as e:
        print(e)


# Function to call the NLPModel class and build a doc2vec model trained on the harvested data stored in sql database
@app.route('/generate_report', methods=['POST', 'GET'])
def generate_report():
    try:
        input_query = request.files
        uploaded_file = input_query['file']
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine="xlsxwriter")
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
            MuserReport(file_path, writer)
            writer.save()
            print("Workbook saved")
            output.seek(0)
            print("Output mapped to the starting index")
            # response = Response(self.output.getvalue(),
            #                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            #                     headers={"Content-Disposition": "attachment;filename=Dss_project.txt"},
            #                     content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            # print("response created")
            print("Response received")
        return send_file(output, attachment_filename="muser_report.xlsx", as_attachment=True)

    except Exception() as e:
        print(e)

