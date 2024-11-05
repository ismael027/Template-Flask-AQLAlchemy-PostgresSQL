from flask import Blueprint
from kanban.card.view.card_view import get_cards, create_card, update_card, delete_card
from kanban.utils import required_fields

card_bp = Blueprint('card', __name__)

@card_bp.route('/card/<user_id>', methods=['GET'])
def get_cards_view(user_id):
    return get_cards(user_id)

@card_bp.route('/card/<user_id>', methods=['POST'])
@required_fields('title', 'category_id', 'status', 'description')
def create_card_view(user_id):
    return create_card(user_id)

@card_bp.route('/card/<id>', methods=['PATCH'])
@required_fields('status', 'title', 'category_id', 'description')
def update_card_view(id):
    return update_card(id)

@card_bp.route('/card/<id>', methods=['DELETE'])
def delete_card_view(id):
    return delete_card(id)