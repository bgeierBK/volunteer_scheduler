from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from config import db, bcrypt

user_school_association = db.Table('user_school_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users_table.id'), primary_key=True),
    db.Column('school_id', db.Integer, db.ForeignKey('schools_table.id'), primary_key=True),
    ForeignKeyConstraint(['user_id'], ['users_table.id'], name='fk_user_id'),  
    ForeignKeyConstraint(['school_id'], ['schools_table.id'], name='fk_school_id') 
     )

class User(db.Model, SerializerMixin):
    __tablename__ = 'users_table'

    id = db.Column(db.Integer, primary_key =True)
    fullName = db.Column(db.String, unique =True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    childsClass = db.Column(db.String, nullable=False )
    _hashed_password = db.Column(db.String, nullable=False)
   
    shifts = db.relationship('Shift', back_populates='user')
    schools = db.relationship('School', secondary=user_school_association, back_populates='schools')

class Month(db.Model, SerializerMixin):
    __tablename__ = 'months_table'

    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String, unique =True, nullable=False)
    notes = db.Column(db.String)

class Shift(db.Model, SerializerMixin):
    __tablename__ = 'shifts_table'

    id = db.Column(db.Integer, primary_key =True)
    description = db.Column(db.String, nullable=False)
    day = db.Column(db.String, nullable=False)
    startTime = db.Column(db.String, nullable = False)
    endTime = db.Column(db.String, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('users_table.id'), nullable=False)
    user=db.relationship('User', back_populates='shift')



class School(db.Model, SerializerMixin):
    __tablename__ = 'schools_table'

    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String, nullable = False)
    _hashed_accessCode = db.Column(db.String, nullable = False)

    users = db.relationship('User', secondary=user_school_association, back_populates='schools')
    
     
     
     


