# bakend/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import uuid

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    verification_code = db.Column(db.String(36), unique=True, nullable=True)
    # --- NUEVO CAMPO: ROLE ---
    role = db.Column(db.String(20), default='user', nullable=False) # 'user' o 'admin'

    avatar = db.relationship('Avatar', backref='user', lazy=True, uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

class Avatar(db.Model):
    __tablename__ = 'avatar'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    model_id = db.Column(db.String(100), nullable=False, default='default_robot')
    custom_data = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Avatar User:{self.user_id} Model:{self.model_id}>'