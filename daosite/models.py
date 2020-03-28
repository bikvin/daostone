from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from daosite import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='user')  # admin or user

    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


color_product = db.Table('color_product',
                         db.Column('color_id', db.Integer, db.ForeignKey('color.id'), primary_key=True),
                         db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
                         )

use_product = db.Table('use_product',
                       db.Column('use_id', db.Integer, db.ForeignKey('use.id'), primary_key=True),
                       db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
                       )

material_product = db.Table('material_product',
                            db.Column('material_id', db.Integer, db.ForeignKey('material.id'), primary_key=True),
                            db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
                            )

chipsize_product = db.Table('chipsize_product',
                            db.Column('chipsize_id', db.Integer, db.ForeignKey('chipsize.id'), primary_key=True),
                            db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
                            )

surface_product = db.Table('surface_product',
                           db.Column('surface_id', db.Integer, db.ForeignKey('surface.id'), primary_key=True),
                           db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
                           )

interior_product = db.Table(
    'interior_product',
    db.Column('interior_id', db.Integer, db.ForeignKey('interior.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
)


class Product(db.Model):
    __searchable__ = ['name', 'subname', 'description']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subname = db.Column(db.String(100), nullable=True)
    
    price_currency = db.Column(db.String(3), nullable=True)
    price_unit = db.Column(db.String(10), nullable=True)
    price = db.Column(db.Float, nullable=True)
    discount = db.Column(db.Float, nullable=True)

    active = db.Column(db.Boolean, default=False, nullable=False)

    popular = db.Column(db.Boolean, default=False, nullable=True)

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=True)

    image_1_file_path = db.Column(db.String(500), nullable=True)
    image_2_file_path = db.Column(db.String(500), nullable=True)
    image_3_file_path = db.Column(db.String(500), nullable=True)
    image_4_file_path = db.Column(db.String(500), nullable=True)
    image_5_file_path = db.Column(db.String(500), nullable=True)

    thumb50_1_file_path = db.Column(db.String(500), nullable=True)
    thumb50_2_file_path = db.Column(db.String(500), nullable=True)
    thumb50_3_file_path = db.Column(db.String(500), nullable=True)
    thumb50_4_file_path = db.Column(db.String(500), nullable=True)
    thumb50_5_file_path = db.Column(db.String(500), nullable=True)

    thumb100_1_file_path = db.Column(db.String(500), nullable=True)
    thumb100_2_file_path = db.Column(db.String(500), nullable=True)
    thumb100_3_file_path = db.Column(db.String(500), nullable=True)
    thumb100_4_file_path = db.Column(db.String(500), nullable=True)
    thumb100_5_file_path = db.Column(db.String(500), nullable=True)

    thumb270_1_file_path = db.Column(db.String(500), nullable=True)
    thumb270_2_file_path = db.Column(db.String(500), nullable=True)
    thumb270_3_file_path = db.Column(db.String(500), nullable=True)
    thumb270_4_file_path = db.Column(db.String(500), nullable=True)
    thumb270_5_file_path = db.Column(db.String(500), nullable=True)

    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    width_mm = db.Column(db.Integer, nullable=True)
    length_mm = db.Column(db.Integer, nullable=True)
    height_mm = db.Column(db.Integer, nullable=True)

    weight_kg = db.Column(db.Float, nullable=True)

    colors = db.relationship('Color', secondary=color_product, lazy='subquery',
                             backref=db.backref('products', lazy=True))

    uses = db.relationship('Use', secondary=use_product, lazy='subquery',
                           backref=db.backref('uses', lazy=True))

    materials = db.relationship('Material', secondary=material_product, lazy='subquery',
                                backref=db.backref('materials', lazy=True))

    chipsizes = db.relationship('Chipsize', secondary=chipsize_product, lazy='subquery',
                                backref=db.backref('chipsizes', lazy=True))

    surfaces = db.relationship('Surface', secondary=surface_product, lazy='subquery',
                               backref=db.backref('surfaces', lazy=True))

    interior = db.relationship('Interior', secondary=interior_product, lazy='subquery',
                               backref=db.backref('interiors', lazy=True))

    @property
    def get_price(self):
        return self.price

    def calculate_discount(self, price, discount):
        if discount:
            return price - (price / 100 * discount)
        return price

    @property
    def get_actual_price(self):
        price = self.get_price
        return self.calculate_discount(price, self.discount)

    @property
    def get_unit_price(self):
        price = self.get_price
        if self.price_unit == 'm2' and self.price and self.width_mm and self.length_mm:
            price = price * (self.width_mm * self.length_mm / 1000000)
        return price

    @property
    def get_unit_actual_price(self):
        price = self.get_unit_price
        return self.calculate_discount(price, self.discount)

    @property
    def get_m2_price(self):
        price = self.get_price
        if self.price_unit == 'unit':
            price = self.price / (self.width_mm * self.length_mm / 1000000)
        return price

    @property
    def get_m2_actual_price(self):
        price = self.get_m2_price
        return self.calculate_discount(price, self.discount)


class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url_name = db.Column(db.String(100), nullable=False)
    page_title = db.Column(db.String(100), nullable=False)
    header_title = db.Column(db.String(100), nullable=False)
    meta_description = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)


class Use(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url_name = db.Column(db.String(100), nullable=False)
    page_title = db.Column(db.String(100), nullable=False)
    header_title = db.Column(db.String(100), nullable=False)
    meta_description = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url_name = db.Column(db.String(100), nullable=False)
    page_title = db.Column(db.String(100), nullable=False)
    header_title = db.Column(db.String(100), nullable=False)
    meta_description = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)


class Chipsize(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url_name = db.Column(db.String(100), nullable=False)
    page_title = db.Column(db.String(100), nullable=False)
    header_title = db.Column(db.String(100), nullable=False)
    meta_description = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)


class Surface(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url_name = db.Column(db.String(100), nullable=False)
    page_title = db.Column(db.String(100), nullable=False)
    header_title = db.Column(db.String(100), nullable=False)
    meta_description = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    info = db.Column(db.Text, nullable=True)
    page_title = db.Column(db.String(100), nullable=False)
    header_title = db.Column(db.String(100), nullable=False)
    meta_description = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    files_directory = db.Column(db.String(50), nullable=False)

    products = db.relationship('Product', backref='brand', lazy=True)

    url_name = db.Column(db.String(100), nullable=False)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    files_directory = db.Column(db.String(50), nullable=False)

    products = db.relationship('Product', backref='category', lazy=True)
    url_name = db.Column(db.String(100), nullable=False)


item_order = db.Table('item_order',
                      db.Column('ordered_item_id', db.Integer, db.ForeignKey('ordered_item.id'), primary_key=True),
                      db.Column('online_order_id', db.Integer, db.ForeignKey('online_order.id'), primary_key=True),

                      )

# class Product_order(db.Model):
#     __tablename__ = 'product_order'
#     id = db.Column(db.Integer, primary_key=True)

#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
#     order_id = db.Column(db.Integer, db.ForeignKey('online_order.id'))
#     quantity = db.Column('quantity', db.Integer, nullable=False)


class Ordered_item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)


class Online_order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    delivery = db.Column(db.String(10), nullable=False)
    delivery_price = db.Column(db.Integer, nullable=False)
    ordered_items = db.relationship('Ordered_item', secondary='item_order', lazy='subquery', backref=db.backref('orders', lazy=True))
    order_total = db.Column(db.Float, nullable=False)


class Interior(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    products = db.relationship('Product', secondary='interior_product', lazy='subquery', backref=db.backref('interiors', lazy=True))
    images = db.relationship('InteriorImage', backref='interior', lazy='subquery')

    def __repr__(self):
        return self.name


class InteriorImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    interior_id = db.Column(db.Integer, db.ForeignKey('interior.id'))
    path = db.Column(db.String(500), nullable=True)


class Rate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3), nullable=False, unique=True)
    value = db.Column(db.Float, nullable=False)
