# muser-data-app

This is a Python Flask web app that currently offers the below functionalities:
* The app is now able to extract data from Spotify API, save a raw CSV file with the timestamp, and perform ETL operation to dump the extracted data in SQL Server table.
* In addition to the data extraction functionality, we have incorporated functionality to build a doc2vec NLP model and train it on the data dumped in the SQL table.
* There is one final functionality to expand the muser data, collected from FireBase, with metadata information collected from Spotify. The app first queries Spotify for an exact match with the muser record (artist, track, and album), and in case there is no exact match, the app utilizes the doc2vec model to predict the most similar match in the SQL table.

## Setup

You'll need the following installed to build the project:
* python>=3.6
* pandas>=1.1.3
* textslack>=0.1.5
* gensim>=3.8.1
* numpy>=1.18.4
* flask>=1.1.2
* spotipy>=2.16.1
* python-dotenv>=0.14.0
* sqlalchemy>=1.3.19

## Setup .env file
You'll need a .env file to store all the required credentials

## Setup Spotify Developer Account

Create a Spotify Developer account and generate client id and client secret key.

## Setup a SQL Database

Create a database and run the db_schema.sql file.
Generate a connection string and create a sqlalchemy engine.

## Run

To run the application run the run.py file thorugh command line or an IDE.

## License

```
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
 ```
