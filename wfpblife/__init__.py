import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

from flask import Flask
from flask_bcrypt import Bcrypt
from pymongo import MongoClient



app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
cloudinary.config(
    cloud_name='bogtrotter72',
    api_key=os.getenv('CLOUDINARY_API'),
    api_secret=os.getenv('CLOUDINARY_SECRET')
)

db_user = os.getenv('MONGO_USER')
db_password = os.getenv('MONGO_PASSWORD')
client = MongoClient(f'mongodb+srv://{db_user}:{db_password}@wfpblife-testdb-2x5ke.mongodb.net/test?retryWrites=true&w=majority')
db = client["wfpblife-testdb"]

bcrypt = Bcrypt(app)

from wfpblife import routes