from daosite import create_app
app = create_app()
app.app_context().push()

from daosite import db
from daosite.models import User, Post, Product, Brand, Color, Chipsize, Category, Use
from daosite import bcrypt
