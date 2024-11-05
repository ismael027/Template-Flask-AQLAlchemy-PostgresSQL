from datetime import datetime
from uuid import uuid4

from flask import jsonify, request
from sqlalchemy import select

from kanban.database import Session
from kanban.categories.model.categories_model import Category
from kanban.user.model.user_model import User

def get_cards_categories(user_id):
    with Session() as session:
        query = select(User).where(User.id == user_id)
        user = session.scalars(query).first()
        if user is None:
            return jsonify({'error': 'invalid user_id'}), 400

        query = select(Category).where(Category.user_id == user.id)
        cards_Category = [
            card_category.to_dict()
            for card_category in session.scalars(query).all()
        ]
        return jsonify(cards_Category)


def create_card_category(user_id):
    with Session() as session:
        query = select(User).where(User.id == user_id)
        user = session.scalars(query).first()
        if user is None:
            return jsonify({'error': 'invalid user_id'}), 400

        card_category = Category(
            name=request.json['name'],
            color=request.json['color'], 
            user_id=user.id,
            id=str(uuid4())
        )
        session.add(card_category)
        session.commit()
        session.flush()
        return jsonify(card_category.to_dict())

def delete_card_category(id):
    with Session() as session:
        query = select(Category).where(Category.id == id)
        card_category = session.scalars(query).first()
        if card_category is None:
            return jsonify({'error': 'Card category not found'}), 404
        session.delete(card_category)
        session.commit()
        session.flush()
        return jsonify({'message': 'Category deleted successfully'})