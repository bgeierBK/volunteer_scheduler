from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import db, bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
CORS(app)  

db.init_app(app)  
migrate = Migrate(app, db)

from models import User  

@app.route('/')
def index():
    return "Hello, this is the homepage!"

if __name__ == '__main__':
    app.run(debug=True)
