import os
from flask import Flask
from pymongo import MongoClient


app = Flask(__name__)
app.config['SECRET_KEY'] = '27f2c2c1830938f3660c867a93f845c2'

db_user = os.getenv('MONGO_USER')
db_password = os.getenv('MONGO_PASSWORD')
client = MongoClient(f'mongodb+srv://{db_user}:{db_password}@wfpb-life-mr6o4.mongodb.net/test?retryWrites=true&w=majority')
db = client["wfpb-life"]

from wfpblife import routes