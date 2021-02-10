# Import the dependencies
from flask import Flask
from dotenv import load_dotenv
import os

# Sets the correct .env file
load_dotenv(os.path.join(os.getcwd(), '.env'))

# Creates a flask app
app = Flask(__name__)

# Makes call to the config file
app.secret_key = os.environ.get('SECRET_KEY')
if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")
else:
    app.config.from_object("config.ProductionConfig")

# Imports the view.py file
from app import view
