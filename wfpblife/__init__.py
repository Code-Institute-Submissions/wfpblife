import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

from flask import Flask
from flask_bcrypt import Bcrypt
from pymongo import MongoClient



app = Flask(__name__)
app.config['SECRET_KEY'] = '7fa953dcdd7a296edab71c7579cdd8fc'
cloudinary.config(
    cloud_name='bogtrotter72',
    api_key='853615826873476',
    api_secret='N6Dn0sE1Ns6NrP5IMbsAAy7aQlc'
)

db_user = os.getenv('MONGO_USER')
db_password = os.getenv('MONGO_PASSWORD')
client = MongoClient(f'mongodb+srv://{db_user}:{db_password}@wfpblife-testdb-2x5ke.mongodb.net/test?retryWrites=true&w=majority')
db = client["wfpblife-testdb"]

bcrypt = Bcrypt(app)

from wfpblife import routes