from flask import Flask, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import db, bcrypt
from models import User, School, Month, Shift

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

## login routes

@app.post('/api/users')
def create_user():
    try:
        new_user = User(
            fullName = request.json.get('username'),
            email = request.json.get('email'),
        )
        new_user.hashed_password = bcrypt.generate_password_hash(request.json.get('password')).decode('utf-8')
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        return new_user.to_dict(), 201

    except Exception as e:
        return {'error': str(e)}, 406

@app.get('/api/check_session')
def check_session():
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        if user:
            return user.to_dict(), 200
        else:
            return {'error': 'user not found'}, 404
    else:
        return {'error': 'no active session'}, 204

@app.post('/api/login')
def login():
    user = User.query.where(User.email == request.json.get('email')).first()
    if user and bcrypt.check_password_hash(user._hashed_password, request.json.get('password')):
        session['user_id'] = user.id
        return user.to_dict(), 201
    else:
        return {'error': 'Username or password was invalid'}

@app.delete('/api/logout')
def logout():
    session.pop('user_id', None)
    return {}, 204


