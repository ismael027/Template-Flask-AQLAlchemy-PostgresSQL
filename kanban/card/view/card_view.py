from datetime import datetime
from uuid import uuid4

from flask import jsonify, request
from sqlalchemy import select

from kanban.database import Session
from kanban.card.model.card_model import Card
from kanban.user.model.user_model import User
from kanban.categories.model.categories_model import Category

def get_cards(user_id):
    with Session() as session:
        query = select(User).where(User.id == user_id)
        user = session.scalars(query).first()
        if user is None:
            return jsonify({'error': 'invalid user_id'}), 400

        query = select(Card).where(Card.user_id == user.id)
        cards = [card.to_dict() for card in session.scalars(query).all()]
        return jsonify(cards)

def create_card(user_id):
    with Session() as session:
        query = select(User).where(User.id == user_id)
        user = session.scalars(query).first()
        if user is None:
            return jsonify({'error': 'invalid user_id'}), 400

        category_ids = request.json['category_id']
        categories = session.scalars(select(Category).where(Category.id.in_(category_ids))).all()
        if not categories:
            return jsonify({'error': 'Invalid category_ids'}), 400

        card = Card(
            status=request.json['status'],
            title=request.json['title'],
            description=request.json.get('description'),
            id=str(uuid4()),
            user_id=user.id,
        )
        card.categories.extend(categories)

        session.add(card)
        session.commit()
        session.flush()
        return jsonify(card.to_dict())

def update_card(id):
    with Session() as session:
        query = select(Card).where(Card.id == id)
        card = session.scalars(query).first()
        if card is None:
            return jsonify({'error': 'Card not found'}), 404

        category_ids = request.json['category_id']
        categories = session.scalars(select(Category).where(Category.id.in_(category_ids))).all()
        if not categories:
            return jsonify({'error': 'Invalid category_ids'}), 400

        card.status = request.json['status']
        card.title = request.json['title']
        card.description = request.json.get('description')
        card.update_at = datetime.now()

        card.categories.clear()
        card.categories.extend(categories)

        session.commit()
        session.flush()
        return jsonify(card.to_dict())


def delete_card(id):
    with Session() as session:
        query = select(Card).where(Card.id == id)
        card = session.scalars(query).first()
        if card is None:
            return jsonify({'error': 'Card not found'}), 404
        session.delete(card)
        session.commit()
        session.flush()
        return jsonify({'message': 'Card deleted successfully'})