from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from kanban import views
from kanban.controllers.user_controller import user_bp
from kanban.controllers.card_controller import card_bp
from kanban.controllers.categories_controller import card_category_bp
from kanban.config import get_config
from kanban.extensions import login

from kanban.database import init_db


def create_app():
    app = Flask(__name__)
    app.secret_key = get_config()['SECRET_KEY']
    login.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(card_bp)
    app.register_blueprint(card_category_bp)

    SWAGGER_URL = '/docs'
    API_URL = '/static/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Kanban API"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app


app = create_app()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
