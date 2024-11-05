from flask import Blueprint
from kanban.categories.view.categories_view import get_cards_categories, create_card_category, delete_card_category
from kanban.utils import required_fields

card_category_bp = Blueprint('card_category', __name__)

@card_category_bp.route('/category/<user_id>', methods=['GET'])
def get_cards_categories_view(user_id):
    return get_cards_categories(user_id)

@card_category_bp.route('/category/<user_id>', methods=['POST'])
@required_fields('name', 'color')
def create_card_category_view(user_id):
    return create_card_category(user_id)

@card_category_bp.route('/category/<id>', methods=['DELETE'])
def delete_card_category_view(id):
    return delete_card_category(id)