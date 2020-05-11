import re
import urllib

from werkzeug.datastructures import CombinedMultiDict, MultiDict

from flask import (Blueprint, jsonify, redirect, render_template, request,
                   session, url_for, render_template_string)
from jinja2 import contextfilter

from sqlalchemy import and_

from daosite import db
from daosite.filter.forms import FilterForm
from daosite.dynamic_filter.forms import DynamicFilterForm
from daosite.interiors.routes import interiors_per_page
from daosite.main.forms import OrderForm, SearchForm
from daosite.main.utils import (add_to_cart_session, get_rates,
                                send_admin_email, send_user_email)
from daosite.models import (Brand, Category, Color, Interior, Material,
                            Online_order, Ordered_item, Product, Rate, Use, Slider, Content, GroupFlag, Flag)

main = Blueprint('main', __name__)


@main.route("/")
def home():
    slider = Slider.query.filter(Slider.active == True).order_by(Slider.order_id.asc())
    popular_products = Product.query.filter(Product.popular == True, Product.active == True)
    discount_products = Product.query.filter(Product.discount > 0, Product.active == True).order_by(Product.id.desc()).limit(8)
    header_title = "Daostone.ru - магазин мозаики для отделки. Лучшая мозаика для вашего интерьера."
    return render_template('home.html', popular_products=popular_products, discount_products=discount_products, header_title=header_title, slider=slider)


@main.route("/products")
def products(*add_dict_args):
    page = request.args.get('page', 1, type=int)
    per_page = 18
    discount = request.args.get('discount', False, type=bool)
    page_title = "" # "Вся мозаика"
    header_title = "" # 'Вся мозаика - Daostone.ru'
    meta_description = "" # 'вся мозаика'
    description = ''

    products = Product.query.filter(Product.active == True)

    # .order_by(Product.id.desc()).paginate(page=page, per_page=18)
    # for test
    # args_dict = request.args.to_dict(flat=False)
    # # args_dict['categories'].append('2')
    # tmp = MultiDict([add_dict_args])
    args = request.args

    # categories = args.getlist('categories')
    # if categories:
    #     products = products.join(Category).filter(
    #         Category.id.in_(categories)
    #     )

    # manufacturers = args.getlist('manufacturers')
    # if manufacturers:
    #     products = products.join(Brand).filter(
    #         Brand.id.in_(manufacturers)
    #     )
        
    # data_dict = []
    # if len(args) > 0:
    #     categories = args.getlist('categories')

    #     for category_name in categories:
    #         if not category_name.isnumeric():
    #             category = Category.query.filter(Category.url_name == category_name).first()

    #             if category: 
    #                 data_dict.append(('categories', str(category.id)) )

    #                 # break

    if not add_dict_args == () and len(add_dict_args) > 0:
        args = CombinedMultiDict([request.args, MultiDict(add_dict_args[0]) ])

    # if len(data_dict) > 0:
    #     args = CombinedMultiDict([request.args, MultiDict([data_dict[0]]) ])

    filter_form = DynamicFilterForm(args, query=products, csrf_enabled=False)
    if filter_form.validate():
        products = filter_form.filter_query(products)

    if discount:
        products = products.filter(Product.discount > 0)
        per_page = 50

    items = products.order_by(Product.id.desc()).paginate(page=page, per_page=per_page)
    ctx = {
        'products': items,
        'filter_form': filter_form,
        'page_title': page_title,
        'header_title': header_title,
        'meta_description': meta_description,
        'description': description,
    }
    return render_template('products.html', **ctx)


@main.route("/categories/<string:select_category>", defaults={'selection': None})
@main.route("/categories/<string:select_category>/<string:selection>")
@main.route("/products/categories/<string:select_category>", defaults={'selection': None})
@main.route("/products/categories/<string:select_category>/<string:selection>")
@main.route("/products/<string:select_category>", defaults={'selection': None})
@main.route("/products/<string:select_category>/<string:selection>")
def products_selected_additional(select_category, selection = ""):
    return products_selected(select_category, selection)


@main.route("/<string:select_category>/<string:selection>/filtered")
def products_selected(select_category, selection = ""):



    
    # args = request.args
    # = category.id
    data_dict = []
    if select_category == 'brand' and not selection == "":
        brand = Brand.query.filter(Brand.url_name == selection).first()
        if brand:
            data_dict = [('manufacturers', str(brand.id))]
    else:    
        category = Category.query.filter(Category.url_name == select_category).first()
        if category:
            data_dict = [('categories', str(category.id))]
        # else:
        #     return None;

        if not selection == "":
            flag = Flag.query.filter(Flag.url_name == selection).first()
            if flag:
                data_dict.append( ('flags', str(flag.id)) )

    return products( data_dict )

@main.route("/<string:select_category>/all")
def products_category(select_category):
    return products_selected(select_category)

@main.route("/mosaic")
def mosaic():
    page = request.args.get('page', 1, type=int)
    per_page = 18
    discount = request.args.get('discount', False, type=bool)
    mosaic_category = Category.query.filter(Category.url_name == 'mosaic').first()

    page_title = "Вся мозаика"
    header_title = 'Вся мозаика - Daostone.ru'
    meta_description = 'вся мозаика'
    description = ''

    products = Product.query.filter(Product.active == True)

    if mosaic_category:
        products = products.filter(Product.category_id == mosaic_category.id)
    filter_form = FilterForm(request.args, csrf_enabled=False)
    if filter_form.validate():
        products = filter_form.filter_query(Product.query.filter(Product.active == True))
    if discount:
        products = products.filter(Product.discount > 0)
        per_page = 50
    
    mosaics = products.order_by(Product.id.desc()).paginate(page=page, per_page=per_page)
    ctx = {
        'mosaics': mosaics,
        'filter_form': filter_form,
        'page_title': page_title,
        'header_title': header_title,
        'meta_description': meta_description,
        'description': description,
    }
    return render_template('mosaic.html', **ctx)


@main.route("/mosaic/<string:select_category>/<string:selection>")
def mosaic_selected(select_category, selection):

    return products_selected('mosaic', selection)
    page = request.args.get('page', 1, type=int)

    mosaic_category = Category.query.filter(Category.url_name == 'mosaic').first()

    if select_category == 'brand':
        brand = Brand.query.filter(Brand.url_name == selection).first()

        products = Product.query.filter(Product.brand_id == brand.id).filter(Product.active == True).filter(Product.category_id == mosaic_category.id)

        #title = 'Производитель мозаики: ' + brand.name
        title = 'Производитель мозаики: ' + brand.name
        header_title = brand.header_title
        page_title = brand.page_title
        meta_description = brand.meta_description
        description = brand.description

    elif select_category == 'material':
        material = Material.query.filter(Material.url_name == selection).first()
        products = Product.query.filter(Product.active == True).filter(Product.category_id == mosaic_category.id).join(Material, Product.materials).filter(Material.url_name == selection)
        title = 'Материал мозаики: ' + Material.query.filter(Material.url_name == selection).first().name
        header_title = material.header_title
        page_title = material.page_title
        meta_description = material.meta_description
        description = material.description

    elif select_category == 'use':
        use = Use.query.filter(Use.url_name == selection).first()
        products = Product.query.filter(Product.active == True).filter(Product.category_id == mosaic_category.id).join(Use, Product.uses).filter(Use.url_name == selection)
        #title = 'Применение мозаики: ' + Use.query.filter(Use.url_name == selection).first().name
        title = 'Применение мозаики: ' + use.name
        header_title = use.header_title
        page_title = use.page_title
        meta_description = use.meta_description
        description = use.description

    elif select_category == 'color':
        color = Color.query.filter(Color.url_name == selection).first()
        products = Product.query.filter(Product.active == True).filter(Product.category_id == mosaic_category.id).join(Color, Product.colors).filter(Color.url_name == selection)
        title = 'Цвет мозаики: ' + Color.query.filter(Color.url_name == selection).first().name
        header_title = color.header_title
        page_title = color.page_title
        meta_description = color.meta_description
        description = color.description

    else:
        products = Product.query.order_by(Product.id.desc()).paginate(page=page, per_page=18)
    
    filter_form = FilterForm(request.args, query=products, csrf_enabled=False)
    if filter_form.validate():
        products = filter_form.filter_query(products)
    mosaics = products.order_by(Product.id.desc()).paginate(page=page, per_page=18)
    
    return render_template(
        'mosaic.html',
        mosaics=mosaics,
        filter_form=filter_form,
        page_title=page_title,
        select_category=select_category,
        selection=selection,
        header_title=header_title,
        meta_description=meta_description,
        description=description
    )


@main.route("/single-mosaic/<int:mosaic_id>")
def single_mosaic(mosaic_id):
    mosaic = Product.query.get_or_404(mosaic_id)
    
    groups = []
    for  group in mosaic.category.group_flag:
        for flag in mosaic.flag:
            if flag.group_flag_id == group.id:
                groups.append(group)
                break
        
    header_title = "Мозаика " + mosaic.name + ", Производитель - " + mosaic.brand.name + " - Daostone.ru"

    title = "Товар"

    session['test'] = 'test'

    return render_template(
        'single-mosaic.html',
        mosaic=mosaic,
        title=title,
        header_title=header_title,
        groups = groups
    )


@main.route("/mosaic/discounts")
def mosaic_discount():
    return redirect(url_for('main.products', discount=True))


@main.route("/mosaic/search")
def search_products():
    page = request.args.get('page', 1, type=int)

    page_title = "Вся мозаика"
    header_title = 'Вся мозаика - Daostone.ru'
    meta_description = 'вся мозаика'
    description = ''

    form = SearchForm(request.args)
    if form.validate():
        q = form.q.data
        products = Product.query.msearch(q, fields=['name', 'subname', 'description'])
        mosaics = products.filter().order_by(Product.id.desc()).paginate(page=page, per_page=18)
    else:
        mosaics = Product.query.filter(Product.active == True)

    ctx = {
        'mosaics': mosaics,
        'page_title': page_title,
        'header_title': header_title,
        'meta_description': meta_description,
        'description': description
    }
    return render_template('search_products.html', **ctx)


@main.route("/getsession")
def get_session():
    i = str(session.items())
    print(i)
    return i


@main.route("/dropsession")
def drop_session():
    [session.pop(key) for key in list(session.keys()) if key != '_flashes']
    return "Dropped"


@main.route("/_add_to_cart")
def add_to_cart():

    quantity = request.args.get('quantity', 0, type=int)
    print(quantity)
    id = request.args.get('id', 0, type=int)
    print(id)
    usd_rate = Rate.query.filter(Rate.name == 'usd').first()
    eur_rate = Rate.query.filter(Rate.name == 'eur').first()

    mosaic = Product.query.get(id)

    add_to_cart_session(mosaic, quantity, usd_rate.value, eur_rate.value)

    resp = jsonify(session['cart_items'])
    resp.status_code = 200

    return resp


@main.route("/_get_cart_session")
def get_cart_session():
    if session.get('cart_items') is None:
        print('no cart')
        # session['cart_items'] = []

    resp = jsonify(session['cart_items'])
    resp.status_code = 200
    return resp


@main.route("/_change_qty_in_session")
def change_qty_in_session():

    quantity = request.args.get('quantity', 0, type=int)
    row = request.args.get('row', 0, type=int)

    session['cart_items'][row]['qty'] = quantity
    session.modified = True

    resp = jsonify(session['cart_items'])
    resp.status_code = 200
    return resp


@main.route("/_delete_item_in_session")
def delete_item_in_session():

    # quantity = request.args.get('quantity', 0, type=int)
    row = request.args.get('row', 0, type=int)
    del session['cart_items'][row]
    # session['cart_items'][row]['qty'] = quantity
    session.modified = True

    resp = jsonify(session['cart_items'])
    resp.status_code = 200
    return resp


@main.route("/cart", methods=['GET', 'POST'])
def cart():
    form = OrderForm()
    delivery_price = 1000
    free_delivery_threshold = 30000
    print(form.validate_on_submit())
    print(form.errors)
    if form.validate_on_submit():

        order_total = 0

        if form.delivery.data == 'mkad':
            delivery_price = 1000
        else:
            delivery_price = 0
        order = Online_order(name=form.name.data, phone=form.phone.data, email=form.email.data, address=form.address.data, comment=form.comment.data, delivery=form.delivery.data, delivery_price=delivery_price, order_total=0)

        # db.session.commit()

        for item in session['cart_items']:
            product = Product.query.get(item['id'])

            ordered_item = Ordered_item(product_id=product.id, product_name=product.name, quantity=item['qty'], unit_price=item['unit_price'])
            order.ordered_items.append(ordered_item)
            db.session.add(ordered_item)
            order_total = order_total + item['qty'] * item['unit_price']

        if order_total > free_delivery_threshold:
            delivery_price = 0
            order.delivery_price = delivery_price

        order_total = order_total + delivery_price
        order.order_total = order_total
        print(order_total)
        print(order.order_total)

        db.session.add(order)
        db.session.commit()

        if re.match(r"[^@]+@[^@]+\.[^@]+", form.email.data):
            print ('VALID EMAIL')
            send_user_email(form.email.data, form.name.data, order.id)
        # if form.email.data:
            # send_user_email(form.email.data, form.name.data, order.id)

        send_admin_email(order)

        return redirect(url_for('main.order_received'))

    # print('no submit')
    return render_template('cart.html', title='Корзина', form=form, delivery_price=delivery_price, free_delivery_threshold=free_delivery_threshold)


@main.route("/order_received")
def order_received():
    return render_template('order_received.html')


@main.route("/delivery")
def delivery():
    #header_title = 'Доставка и самовывоз - Daostone.ru'
    #return render_template('delivery.html', header_title=header_title)
    header_title = 'Доставка и самовывоз - Daostone.ru'
    content = Content.query.filter(Content.site_var == '@DeliveryContent').first()
    content_html = ''
    if content != None and content.value != None and content.value != 'None' :
        # content_html = content.value
        content_html = render_template_string(content.value)
        return render_template('dynamic_delivery.html', header_title=header_title, content_html=content_html)
    else:
        return render_template('delivery.html', header_title=header_title)

@main.route("/contacts")
def contacts():
    #header_title = 'Контактная информация - Daostone.ru'
    #return render_template('contacts.html', header_title=header_title)
    header_title = 'Контактная информация - Daostone.ru'
    content = Content.query.filter(Content.site_var == '@ContactsContent').first()
    content_html = ''
    if content != None and content.value != None and content.value != 'None' :
        # content_html = content.value
        content_html = render_template_string(content.value)
        return render_template('dynamic_contacts.html', header_title=header_title, content_html=content_html)
    else:
        return render_template('contacts.html', header_title=header_title)

@main.route("/about")
def about():
    header_title = 'О нас - Daostone.ru'
    content = Content.query.filter(Content.site_var == '@AboutContent').first()
    content_html = ''
    if content != None and content.value != None and content.value != 'None' :
        content_html = render_template_string(content.value)
        # content_html = content.value
        return render_template('dynamic_about.html', header_title=header_title, content_html=content_html)
    else:
        return render_template('about.html', header_title=header_title)
    # return render_template('about.html', header_title=header_title)


@main.route("/interiors")
def interiors():
    header_title = 'Интерьеры с мозаикой - Daostone.ru'
    page = request.args.get('page', 1, type=int)
    interiors = Interior.query.order_by(Interior.id.asc()).paginate(page=page, per_page=interiors_per_page)
    return render_template('interiors.html', header_title=header_title, interiors=interiors)


@main.context_processor
def context_processor():
    _rates = Rate.query.all()
    rates = dict()
    for rate in _rates:
        rates[rate.name] = rate.value

    return dict(materials=Material.query.all(),
                brands=Brand.query.all(),
                uses=Use.query.all(),
                colors=Color.query.all(),
                rates=rates,
                categories = Category.query.all(),
                group_flags = GroupFlag.query.filter(GroupFlag.is_topmenu_show == True, GroupFlag.active == True).all()
                )

@main.context_processor
def utility_processor():
    def flugs_name_by_group(product, group_id):
        
        return [flag.name for flag in product.flag if flag.group_flag_id == group_id ]
#     def get_m2_actual_price(product, price=None):
        
#         price = product.price

#         if price != None:
#             price = price
        
#         if product.price_unit == 'unit':
#             price = product.price / (product.width_mm * product.length_mm / 1000000)

#         # price = self.get_m2_price
#         return product.calculate_discount(price, product.discount)

#     def get_unit_actual_price(product, price=None):
        
#         price = product.price

#         if price != None:
#             price = price

#         if product.price_unit == 'm2' and product.price and product.width_mm and product.length_mm:
#             price = price * (product.width_mm * product.length_mm / 1000000)  

#         return product.calculate_discount(price, product.discount)

#     return dict(get_m2_actual_price=get_m2_actual_price, get_unit_actual_price=get_unit_actual_price)
    return dict(flugs_name_by_group=flugs_name_by_group)

@main.app_template_filter('currency_price')
# @contextfilter
def to_price(value, rates, currency = 'rur'):
        if currency == 'rur':
            return value
        elif currency == 'usd':
            return value * rates['usd']
        elif currency == 'eur':
            return value * rates['eur']
            
