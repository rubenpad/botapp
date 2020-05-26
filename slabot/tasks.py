"""Define task to run with celery"""
import os
import json
from random import choice
from bson.json_util import dumps
from celery import Celery
from dotenv import load_dotenv
from pymongo import MongoClient

# Celery settings
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')

# Mongo connection settings
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')

app = Celery(
    'tasks',
    broker=CELERY_BROKER_URL,
    backend=CELERY_BROKER_URL
)
app.conf.timezone = 'America/Bogota'


@app.task(name='savequote')
def savequote(data):
    """Task to save a quote in database"""
    # Create a new quote
    with MongoClient(MONGO_URI) as connection:
        # Connect to database an save data
        database = connection.quotes_db
        database.quotes.insert_one(data)
    return True


@app.task(name='quote')
def quote():
    """Task to give a quote to the user"""
    # Find quotes
    with MongoClient(MONGO_URI) as connection:
        # Connect to database and get data
        database = connection.quotes_db

        # Decoded cursor object to json
        data = dumps(database.quotes.find())

        # Transform quotes json into a list
        quotes_list = json.loads(data)

        # Choose a random quote
        random_quote = choice(quotes_list)

    return {
        'author': random_quote['author'],
        'quote': random_quote['quote'],
    }
