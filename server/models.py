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
    schools = db.relationship('School', secondary=user_school_association, back_populates='users')

    @hybrid_property
    def hashed_password(self):
        raise AttributeError('Password hashes may not be viewed')
    
    @hashed_password.setter
    def hashed_password(self, password):
        hashed_password = bcrypt.generate_password_hash(
        (password).encode('utf-8'))
        self._hashed_password=hashed_password

class School(db.Model, SerializerMixin):
    __tablename__ = 'schools_table'

    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String, nullable = False)
    _hashed_accessCode = db.Column(db.String, nullable = False)

    users = db.relationship('User', secondary=user_school_association, back_populates='schools')
    months = db.relationship('Month', back_populates='school')

    @hybrid_property
    def hashed_accessCode(self):
        raise AttributeError('Access Code hashes may not be viewed')
    
    @hashed_accessCode.setter
    def hashed_accessCode(self, password):
        hashed_accessCode = bcrypt.generate_password_hash(
        (password).encode('utf-8'))
        self._hashed_accessCode=hashed_accessCode

class Month(db.Model, SerializerMixin):
    __tablename__ = 'months_table'

    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String, unique =True, nullable=False)
    notes = db.Column(db.String)
    
    school_id= db.Column(db.Integer, db.ForeignKey('schools_table.id'), nullable=False, name='fk_month_school_id')

    shifts = db.relationship('Shift', back_populates='month')
    school = db.relationship('School', back_populates='months')

class Shift(db.Model, SerializerMixin):
    __tablename__ = 'shifts_table'

    id = db.Column(db.Integer, primary_key =True)
    description = db.Column(db.String, nullable=False)
    day = db.Column(db.String, nullable=False)
    startTime = db.Column(db.String, nullable = False)
    endTime = db.Column(db.String, nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('users_table.id'), nullable=False)
    month_id = db.Column(db.Integer, db.ForeignKey('months_table.id'), nullable=False)

    user=db.relationship('User', back_populates='shifts')
    month=db.relationship('Month', back_populates='shifts')




    
     
     
     


