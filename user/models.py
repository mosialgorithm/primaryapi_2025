from app import db
from sqlalchemy import Column, Integer, String, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



class UserModel(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    username = Column(String(100), nullable=True)
    phone = Column(String(11), unique=True, nullable=False)
    email = Column(String(100), nullable=True)
    password = Column(String(250), nullable=False)
    role = Column(Integer, nullable=False, default=2)
    avatar = Column(String(100), default='/assets/images/avatar.png')
    code = Column(String(6), nullable=True)
    code_expire = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    def __init__(self):
        if self.username is None:
            self.username = f'user-{self.phone}'
            
    def __repr__(self):
        return f"{self.name} :: {self.phone}"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_superuser(self):
        return self.role == 0
    
    def is_admin(self):
        return self.role == 1
    