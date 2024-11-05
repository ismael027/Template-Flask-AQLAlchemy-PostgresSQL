from datetime import datetime
from uuid import uuid4

from flask import jsonify, request
from sqlalchemy import select

from kanban.database import Session
from kanban.user.model.user_model import User
from bcrypt import gensalt, hashpw, checkpw

def login():
    email = request.json['email']
    password = request.json['password'].encode('utf-8')
    
    with Session() as session:
        query = select(User).where(User.email == email)
        user = session.scalars(query).first()
        
        if user and checkpw(password, user.password.encode('utf-8')):
            return jsonify({'message': 'Login successful', 'id': user.id}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

def get_user(id):
    with Session() as session:
        query = select(User).where(User.id == id)
        user = session.scalars(query).first()
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict())

def create_user():
    with Session() as session:
        existing_user_query = select(User).where(User.email == request.json['email'])
        existing_user = session.scalars(existing_user_query).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400

        salt = gensalt(8)
        password = hashpw(
            request.json['password'].encode('utf-8'), salt
        ).decode('utf-8')
        user_uuid = str(uuid4())
        user = User(
            id=user_uuid,
            name=request.json['name'],
            email=request.json['email'],
            password=str(password),
            photo=request.json.get('photo'),
        )
        session.add(user)
        session.commit()
        session.flush()
        return jsonify(user.to_dict())
        
def update_user(id):
    with Session() as session:
        query = select(User).where(User.id == id)
        user = session.scalars(query).first()
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        salt = gensalt(8)
        password = hashpw(
            request.json['password'].encode('utf-8'), salt
        ).decode('utf-8')
        user.name = request.json['name']
        user.password = password
        user.email = request.json['email']
        user.photo = request.json.get('photo')
        user.update_at = datetime.now()
        session.commit()
        session.flush()
        return jsonify(user.to_dict())

def delete_user(id):
    with Session() as session:
        query = select(User).where(User.id == id)
        user = session.scalars(query).first()
        if user is None:
            return jsonify({'error': 'invalid user_id'}), 400
        session.delete(user)
        session.commit()
        session.flush()
        return jsonify({'message': 'User deleted successfully'})