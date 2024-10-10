from app import app
from models import User, School
from faker import Faker
from config import db, bcrypt  
from datetime import datetime

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")

        
        User.query.delete()
        School.query.delete()

        
        users = []
        schools=[]

        
        u = User(
            fullName='Reginald VelJonson',
            email='reggie@gmail.com',
            childsClass='k-4',
            _hashed_password=bcrypt.generate_password_hash('password').decode('utf-8')  
        )
        users.append(u)

        s = School(name='PS 666', _hashed_accessCode=bcrypt.generate_password_hash('password').decode('utf-8'))
        schools.append(s)

       
        db.session.add_all(users)
        db.session.add_all(schools)
        db.session.commit()

        print("Seeding complete!")
