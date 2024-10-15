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
        new_user.hashed_password=request.json.get('password')
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

## user routes

@app.get('/api/users')
def get_users():
    return [user.to_dict() for user in User.query.all()], 200

@app.get('/api/users/<int:id>')
def get_one_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict()), 200
    return {}, 404

@app.patch('/api/users/<int:id>')
def update_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        for key, value in request.json.items():
            setattr(user, key, value)
        db.session.commit()
        return {}, 204
    return {}, 404

@app.delete('/api/users/<int:id>')
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return {}, 204
    return {}, 404

## school routes

@app.get('/api/schools')
def get_schools():
    return [school.to_dict() for school in School.query.all()], 200

@app.get('/api/schools/<int:id>')
def get_one_school(id):
    school = School.query.where(School.id == id).first()
    if school:
        return school.to_dict(), 200
    return {}, 400

@app.patch('/api/schools/<int:id>')
def update_school(id):
    school = School.query.where(School.id == id).first()
    if school:
        for key in request.json.keys():
            setattr(school, key, request.json[key])
            db.session.add(school)
            db.sessoin.commit()
            return school.to_dict()
        return {}, 404

@app.delete('/api/schools/<int:id>')
def delete_school(id):
    school = School.query.where(School.id ==id).first()
    if school:
        db.session.delete(school)
        db.session.commit()
        return {}, 204
    return {}, 404

@app.post('/api/schools')
def add_school():
    try:
        new_school = School(
            name = request.json.get('name'),
        )
        new_school.hashed_accessCode=request.json.get('code')
        db.session.add(new_school)
        db.session.commit()
        return new_school.to_dict(), 201
    except Exception as e:
        return {'error': str(e)}, 406