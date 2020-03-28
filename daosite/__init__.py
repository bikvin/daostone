from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_msearch import Search
from flask_sqlalchemy import SQLAlchemy

from daosite.config import Config

db = SQLAlchemy()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    #app = Flask(__name__)
    app = Flask(__name__, static_folder='static', static_url_path='')

    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    search = Search()
    search.init_app(app)
    app.config['MSEARCH_BACKEND'] = 'whoosh'
    app.config['MSEARCH_ENABLE'] = True

    from daosite.users.routes import users
    from daosite.posts.routes import posts
    from daosite.main.routes import main
    from daosite.errors.handlers import errors
    from daosite.products.routes import products
    from daosite.brands.routes import brands
    from daosite.categories.routes import categories
    from daosite.colors.routes import colors
    from daosite.interiors.routes import interiors
    from daosite.rates.routes import rates

    from daosite.uses.routes import uses
    from daosite.materials.routes import materials
    from daosite.chipsizes.routes import chipsizes
    from daosite.surfaces.routes import surfaces
    from daosite.admin.routes import admin
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(products)
    app.register_blueprint(brands)
    app.register_blueprint(categories)
    app.register_blueprint(colors)
    app.register_blueprint(uses)
    app.register_blueprint(materials)
    app.register_blueprint(chipsizes)
    app.register_blueprint(surfaces)
    app.register_blueprint(admin)
    app.register_blueprint(interiors)
    app.register_blueprint(rates)

    return app
