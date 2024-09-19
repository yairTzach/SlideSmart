from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# Replace the URI string with your MongoDB deployment's connection string.
app.config["MONGO_URI"] = "mongodb://localhost:27017/your_database_name"
mongo = PyMongo(app)
