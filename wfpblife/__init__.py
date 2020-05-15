import os
from flask import Flask
from pymongo import MongoClient


app = Flask(__name__)
app.config['SECRET_KEY'] = '7fa953dcdd7a296edab71c7579cdd8fc'

db_user = os.getenv('MONGO_USER')
db_password = os.getenv('MONGO_PASSWORD')
client = MongoClient(f'mongodb+srv://{db_user}:{db_password}@wfpblife-testdb-2x5ke.mongodb.net/test?retryWrites=true&w=majority')
db = client["wfpblife-testdb"]

from wfpblife import routes