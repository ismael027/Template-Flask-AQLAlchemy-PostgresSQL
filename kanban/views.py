from datetime import datetime
from functools import wraps
from uuid import uuid4

from flask import jsonify, request
from sqlalchemy import select

from kanban.database import Session
from kanban.models import Card, CardCategory, User

from bcrypt import gensalt, hashpw

def required_fields(*fields):
    def decorator(function, *args, **kwargs):
        @wraps(function)
        def inner():
            for field in fields:
                if request.json.get(field) is None:
                    return jsonify({'error': f'required field "{field}"'}), 400
            return function(*args, **kwargs)

        return inner

    return decorator


def token_required(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        with Session() as session:
            if request.json.get('user_id') is None:
                return jsonify({'error': 'required field "user_id"'}), 400
            query = select(User).where(User.id == request.json['user_id'])
            user = session.scalars(query).first()
            if user is None:
                return jsonify({'error': 'invalid user_id'}), 400
            return function(*args, **kwargs)

    return decorator


def init_app(app):
    @app.get('/user')
    @token_required
    def get_user():
        with Session() as session:
            query = select(User).where(User.id == request.json['user_id'])
            user = session.scalars(query).first()
            return jsonify(user.to_dict())

    @app.post('/user')
    @required_fields('name', 'email', 'password')
    def create_user():
        with Session() as session:
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

    @app.put('/user')
    @token_required
    @required_fields('name', 'password', 'email')
    def update_user():
        with Session() as session:
            query = select(User).where(User.id == request.json['user_id'])
            user = session.scalars(query).first()
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

    @app.delete('/user')
    @token_required
    def delete_user():
        with Session() as session:
            query = select(User).where(User.id == request.json['user_id'])
            user = session.scalars(query).first()
            session.delete(user)
            session.commit()
            session.flush()
            return jsonify(user.to_dict())

    @app.get('/card')
    @token_required
    def get_cards():
        with Session() as session:
            query = select(User).where(User.id == request.json['user_id'])
            user = session.scalars(query).first()
            query = select(Card).where(Card.user_id == user.id)
            cards = [card.to_dict() for card in session.scalars(query).all()]
            return jsonify(cards)

    @app.get('/card/<card_id>')
    @token_required
    def get_card(card_id):
        with Session() as session:
            query = select(User).where(User.id == request.json['user_id'])
            user = session.scalars(query).first()
            card = session.get(Card, card_id)
            if card and card.user_id == user.id:
                return jsonify(card.to_dict())
            else:
                return jsonify({'error': 'card not found'}), 404

    @app.post('/card')
    @token_required
    @required_fields('title', 'category_id', 'status')
    def create_card():
        with Session() as session:
            query = select(User).where(User.id == request.json['user_id'])
            user = session.scalars(query).first()
            category = session.get(CardCategory, request.json['category_id'])
            if category is None:
                return jsonify({'error': 'invalid category_id'}), 400
            card = Card(
                status=request.json['status'],
                title=request.json['title'],
                description=request.json.get('description'),
                category_id=category.id,
                id=str(uuid4()),
                user_id=user.id,
            )
            session.add(card)
            session.commit()
            session.flush()
            return jsonify(card.to_dict())

    @app.put('/card')
    @token_required
    @required_fields('id', 'status', 'title', 'category_id')
    def update_card():
        with Session() as session:
            card = session.get(Card, request.json['id'])
            '''if request.json['status'] not in ['todo', 'doing', 'done']:
                return (
                    jsonify(
                        {
                            'error': 'card status should only be todo, doing or done'
                        }
                    ),
                    400,
                )'''
            if card:
                card.status = request.json['status']
                card.title = request.json['title']
                card.description = request.json.get('description')
                card.update_at = datetime.now()
                card.category_id = request.json['category_id']
                session.commit()
                session.flush()
                return jsonify(card.to_dict())
            else:
                return jsonify({'error': 'card not found'}), 404

    @app.delete('/card')
    @token_required
    @required_fields('id')
    def delete_card():
        with Session() as session:
            card = session.get(Card, request.json['id'])
            if card is None:
                return jsonify({'error': 'card not found'}), 404
            session.delete(card)
            session.commit()
            session.flush()
            return jsonify(card.to_dict())

    @app.get('/card-category')
    @token_required
    def get_cards_categories():
        with Session() as session:
            query = select(User).where(User.id == request.json['user_id'])
            user = session.scalars(query).first()
            query = select(CardCategory).where(CardCategory.user_id == user.id)
            cards_categories = [
                card_category.to_dict()
                for card_category in session.scalars(query).all()
            ]
            return jsonify(cards_categories)

    @app.get('/card-category/<card_category_id>')
    @token_required
    def get_card_category(card_category_id):
        with Session() as session:
            query = select(User).where(User.id == request.json['user_id'])
            user = session.scalars(query).first()
            card_category = session.get(CardCategory, card_category_id)
            if card_category and card_category.user_id == user.id:
                return jsonify(card_category.to_dict())
            else:
                return jsonify({'error': 'card category not found'}), 404

    @app.post('/card-category')
    @token_required
    @required_fields('name', 'color')
    def create_card_category():
        with Session() as session:
            query = select(User).where(User.id == request.json['user_id'])
            user = session.scalars(query).first()
            card_category = CardCategory(
                name=request.json['name'],
                color=request.json['color'], 
                user_id=user.id,
                id=str(uuid4())
            )
            session.add(card_category)
            session.commit()
            session.flush()
            return jsonify(card_category.to_dict())

    @app.put('/card-category')
    @token_required
    @required_fields('category_id', 'name', 'color')
    def update_card_category():
        with Session() as session:
            card_category = session.get(CardCategory, request.json['category_id'])
            if card_category:
                card_category.name = request.json['name']
                card_category.color = request.json['color']
                card_category.update_at = datetime.now()
                session.commit()
                session.flush()
                return jsonify(card_category.to_dict())
            else:
                return jsonify({'error': 'card category not found'}), 404

    @app.delete('/card-category')
    @token_required
    @required_fields('category_id')
    def delete_card_category():
        with Session() as session:
            card_category = session.get(CardCategory, request.json['category_id'])
            if card_category is None:
                return jsonify({'error': 'card category not found'}), 404
            session.delete(card_category)
            session.commit()
            session.flush()
            return jsonify(card_category.to_dict())
