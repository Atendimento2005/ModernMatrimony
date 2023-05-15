from flask import Flask
from dotenv import load_dotenv
load_dotenv()
import os 

from routes import main

def create_app():

    app = Flask(__name__) 

    # configure db
    app.config['MYSQL_HOST'] = os.environ.get("HOST")
    app.config['MYSQL_PASSWORD'] = os.environ.get("PASSWORD")
    app.config['MYSQL_USER'] = os.environ.get("USERNAME")
    app.config['MYSQL_DB'] = os.environ.get("DATABASE")

    app.register_blueprint(main)

    return app