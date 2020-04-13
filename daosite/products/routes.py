from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from daosite import db
from daosite.models import Product, Brand, Category, Color, Use, Material, Chipsize, Surface, Flag
from daosite.products.forms import ProductForm
from daosite.products.utils import save_product_picture, prepare_file_name, delete_product_picture

products = Blueprint('products', __name__)

products_per_page = 30


@products.route("/product/new", methods=['GET', 'POST'])
@login_required
def new_product():
    flags = Flag.query.all()
    brands = Brand.query.all()
    categories = Category.query.all()
    colors = Color.query.all()
    materials = Material.query.all()
    chipsizes = Chipsize.query.all()
    surfaces = Surface.query.all()
    uses = Use.query.all()
    form = ProductForm()
    form.flags.choices = [(g.id, g.title + " (" + g.group_flag.title + ")") for g in flags]
    form.brand_id.choices = [(g.id, g.name) for g in brands]
    form.category_id.choices = [(g.id, g.name) for g in categories]
    form.colors.choices = [(g.id, g.name) for g in colors]
    form.materials.choices = [(g.id, g.name) for g in materials]
    form.chipsizes.choices = [(g.id, g.name) for g in chipsizes]
    form.surfaces.choices = [(g.id, g.name) for g in surfaces]
    form.uses.choices = [(g.id, g.name) for g in uses]

    if form.validate_on_submit():

        product = Product(category=Category.query.get(form.category_id.data),
                          brand=Brand.query.get(form.brand_id.data),
                          name=form.name.data,
                          subname=form.subname.data,
                          price=form.price.data,
                          discount=form.discount.data,
                          price_currency=form.price_currency.data,
                          price_unit=form.price_unit.data,
                          description=form.description.data,
                          length_mm=form.length_mm.data,
                          width_mm=form.width_mm.data,
                          height_mm=form.height_mm.data,
                          weight_kg=form.weight_kg.data,
                          active=form.active.data,
                          popular=form.popular.data)

        if form.image1.data:
            paths = save_product_picture(form.image1.data, product, 1)
            product.image_1_file_path = paths['image']
            product.thumb50_1_file_path = paths['thumb50']
            product.thumb100_1_file_path = paths['thumb100']
            product.thumb270_1_file_path = paths['thumb270']

        if form.image2.data:
            paths = save_product_picture(form.image2.data, product, 2)
            product.image_2_file_path = paths['image']
            product.thumb50_2_file_path = paths['thumb50']
            product.thumb100_2_file_path = paths['thumb100']
            product.thumb270_2_file_path = paths['thumb270']
        if form.image3.data:
            paths = save_product_picture(form.image3.data, product, 3)
            product.image_3_file_path = paths['image']
            product.thumb50_3_file_path = paths['thumb50']
            product.thumb100_3_file_path = paths['thumb100']
            product.thumb270_3_file_path = paths['thumb270']
        if form.image4.data:
            paths = save_product_picture(form.image4.data, product, 4)
            product.image_4_file_path = paths['image']
            product.thumb50_4_file_path = paths['thumb50']
            product.thumb100_4_file_path = paths['thumb100']
            product.thumb270_4_file_path = paths['thumb270']
        if form.image5.data:
            paths = save_product_picture(form.image5.data, product, 5)
            product.image_5_file_path = paths['image']
            product.thumb50_5_file_path = paths['thumb50']
            product.thumb100_5_file_path = paths['thumb100']
            product.thumb270_5_file_path = paths['thumb270']

        for flag in flags:
            if flag.id in form.flags.data:
                product.flag.append(flag)
            else:
                if flag in product.flag:
                    product.flag.remove(flag)

        for color in colors:
            if color.id in form.colors.data:
                product.colors.append(color)
            else:
                if color in product.colors:
                    product.colors.remove(color)

        for material in materials:
            if material.id in form.materials.data:
                product.materials.append(material)
            else:
                if material in product.materials:
                    product.materials.remove(material)

        for chipsize in chipsizes:
            if chipsize.id in form.chipsizes.data:
                product.chipsizes.append(chipsize)
            else:
                if chipsize in product.chipsizes:
                    product.chipsizes.remove(chipsize)

        for surface in surfaces:
            if surface.id in form.surfaces.data:
                product.surfaces.append(surface)
            else:
                if surface in product.surfaces:
                    product.surfaces.remove(surface)

        for use in uses:
            if use.id in form.uses.data:
                product.uses.append(use)
            else:
                if use in product.uses:
                    product.uses.remove(use)

        db.session.add(product)
        db.session.commit()
        flash('Товар создан', 'success')

        products_qty = Product.query.count()
        last_page = int(products_qty / products_per_page) + 1

        return redirect(url_for('products.product_list', page=last_page))
    return render_template('products/create_product.html', title='Создать мозаику', form=form, legend='Новая мозаика', product=Product())


@products.route("/product_list")
@login_required
def product_list():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.id.asc()).paginate(page=page, per_page=products_per_page)
    # image_thumb_directory = url_for('static', filename="product_pics/" + product.category.files_directory + "/" + product.brand.files_directory + "/" + "thumb50")
    return render_template('products/product_list.html', title='products', products=products)


@products.route("/edit_product/<int:product_id>", methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    # flags = Flag.query.filter( Flag.group_flag.any( Category.any( id =  product.category_id) ) ).all()
    awailible_group_flag_ids = [item.id for item in product.category.group_flag]
    flags = Flag.query.filter(Flag.group_flag_id.in_(awailible_group_flag_ids)).all()
    # flags = Flag.query.all()
    brands = Brand.query.all()
    categories = Category.query.all()
    colors = Color.query.all()
    materials = Material.query.all()
    chipsizes = Chipsize.query.all()
    surfaces = Surface.query.all()
    uses = Use.query.all()
    form = ProductForm()
    form.flags.choices = [(g.id, g.title + " (" + g.group_flag.title + ")") for g in flags]
    form.brand_id.choices = [(g.id, g.name) for g in brands]
    form.category_id.choices = [(g.id, g.name) for g in categories]
    form.colors.choices = [(g.id, g.name) for g in colors]
    form.materials.choices = [(g.id, g.name) for g in materials]
    form.chipsizes.choices = [(g.id, g.name) for g in chipsizes]
    form.surfaces.choices = [(g.id, g.name) for g in surfaces]
    form.uses.choices = [(g.id, g.name) for g in uses]

    if form.validate_on_submit():
        product.category = Category.query.get(form.category_id.data)
        product.brand = Brand.query.get(form.brand_id.data)
        product.name = form.name.data
        product.subname = form.subname.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.price_currency = form.price_currency.data
        product.price_unit = form.price_unit.data
        product.description = form.description.data

        product.length_mm = form.length_mm.data
        product.width_mm = form.width_mm.data
        product.height_mm = form.height_mm.data
        product.weight_kg = form.weight_kg.data

        product.active = form.active.data
        product.popular = form.popular.data

        if form.image1.data:
            paths = save_product_picture(form.image1.data, product, 1)
            product.image_1_file_path = paths['image']
            product.thumb50_1_file_path = paths['thumb50']
            product.thumb100_1_file_path = paths['thumb100']
            product.thumb270_1_file_path = paths['thumb270']

        if form.image2.data:
            # print('image 2 here')
            paths = save_product_picture(form.image2.data, product, 2)
            product.image_2_file_path = paths['image']
            product.thumb50_2_file_path = paths['thumb50']
            product.thumb100_2_file_path = paths['thumb100']
            product.thumb270_2_file_path = paths['thumb270']

        if form.image3.data:
            paths = save_product_picture(form.image3.data, product, 3)
            product.image_3_file_path = paths['image']
            product.thumb50_3_file_path = paths['thumb50']
            product.thumb100_3_file_path = paths['thumb100']
            product.thumb270_3_file_path = paths['thumb270']

        if form.image4.data:
            paths = save_product_picture(form.image4.data, product, 4)
            product.image_4_file_path = paths['image']
            product.thumb50_4_file_path = paths['thumb50']
            product.thumb100_4_file_path = paths['thumb100']
            product.thumb270_4_file_path = paths['thumb270']

        if form.image5.data:
            paths = save_product_picture(form.image5.data, product, 5)
            product.image_5_file_path = paths['image']
            product.thumb50_5_file_path = paths['thumb50']
            product.thumb100_5_file_path = paths['thumb100']
            product.thumb270_5_file_path = paths['thumb270']

        if form.delete_image_1.data:
            delete_product_picture(product.image_1_file_path, product.thumb50_1_file_path, product.thumb100_1_file_path, product.thumb270_1_file_path)
            product.image_1_file_path = None
            product.thumb50_1_file_path = None
            product.thumb100_1_file_path = None
            product.thumb270_1_file_path = None

        if form.delete_image_2.data:

            delete_product_picture(product.image_2_file_path, product.thumb50_2_file_path, product.thumb100_2_file_path, product.thumb270_2_file_path)
            product.image_2_file_path = None
            product.thumb50_2_file_path = None
            product.thumb100_2_file_path = None
            product.thumb270_2_file_path = None

        if form.delete_image_3.data:
            delete_product_picture(product.image_3_file_path, product.thumb50_3_file_path, product.thumb100_3_file_path, product.thumb270_3_file_path)
            product.image_3_file_path = None
            product.thumb50_3_file_path = None
            product.thumb100_3_file_path = None
            product.thumb270_3_file_path = None

        if form.delete_image_4.data:
            delete_product_picture(product.image_4_file_path, product.thumb50_4_file_path, product.thumb100_4_file_path, product.thumb270_4_file_path)
            product.image_4_file_path = None
            product.thumb50_4_file_path = None
            product.thumb100_4_file_path = None
            product.thumb270_4_file_path = None

        if form.delete_image_5.data:
            delete_product_picture(product.image_5_file_path, product.thumb50_5_file_path, product.thumb100_5_file_path, product.thumb270_5_file_path)
            product.image_5_file_path = None
            product.thumb50_5_file_path = None
            product.thumb100_5_file_path = None
            product.thumb270_5_file_path = None

        # print(form.colors.data)

        for flag in flags:
            if flag.id in form.flags.data:
                product.flag.append(flag)
            else:
                if flag in product.flag:
                    product.flag.remove(flag)

        for color in colors:
            if color.id in form.colors.data:
                product.colors.append(color)
            else:
                if color in product.colors:
                    product.colors.remove(color)

        for material in materials:
            if material.id in form.materials.data:
                product.materials.append(material)
            else:
                if material in product.materials:
                    product.materials.remove(material)

        for chipsize in chipsizes:
            if chipsize.id in form.chipsizes.data:
                product.chipsizes.append(chipsize)
            else:
                if chipsize in product.chipsizes:
                    product.chipsizes.remove(chipsize)

        for surface in surfaces:
            if surface.id in form.surfaces.data:
                product.surfaces.append(surface)
            else:
                if surface in product.surfaces:
                    product.surfaces.remove(surface)

        for use in uses:
            if use.id in form.uses.data:
                product.uses.append(use)
            else:
                if use in product.uses:
                    product.uses.remove(use)

        db.session.commit()
        flash('Товар обновлен', 'success')

        products_qty = Product.query.count()
        last_page = int(products_qty / products_per_page) + 1

        return redirect(url_for('products.product_list', page=last_page))

    elif request.method == 'GET':
        form.category_id.data = product.category.id
        form.brand_id.data = product.brand.id
        form.name.data = product.name
        form.subname.data = product.subname
        form.price.data = product.price
        form.discount.data = product.discount
        form.price_currency.data = product.price_currency
        form.price_unit.data = product.price_unit
        form.description.data = product.description
        form.length_mm.data = product.length_mm
        form.width_mm.data = product.width_mm
        form.height_mm.data = product.height_mm
        form.weight_kg.data = product.weight_kg
        form.active.data = product.active
        form.popular.data = product.popular

        form.flags.data = [flag.id for flag in product.flag]

        form.colors.data = [color.id for color in product.colors]
        form.materials.data = [material.id for material in product.materials]
        form.chipsizes.data = [chipsize.id for chipsize in product.chipsizes]
        form.uses.data = [use.id for use in product.uses]
        form.surfaces.data = [surface.id for surface in product.surfaces]

        # image_thumb_directory = url_for('static', filename="product_pics/" + product.category.files_directory + "/" + product.brand.files_directory + "/" + "thumb100")

    return render_template('products/create_product.html', title='Редактирование товара', form=form, legend='Редактирование товара', product=product)


@products.route("/product/<int:product_id>/delete", methods=['POST'])
@login_required
def delete_product(product_id):
    if current_user.status != 'admin':
        abort(403)
    product = Product.query.get_or_404(product_id)

    if product.image_1_file_path:

        delete_product_picture(product.image_1_file_path, product.thumb50_1_file_path, product.thumb100_1_file_path, product.thumb270_1_file_path)
    if product.image_2_file_path:
        delete_product_picture(product.image_2_file_path, product.thumb50_2_file_path, product.thumb100_2_file_path, product.thumb270_2_file_path)
    if product.image_3_file_path:
        delete_product_picture(product.image_3_file_path, product.thumb50_3_file_path, product.thumb100_3_file_path, product.thumb270_3_file_path)
    if product.image_4_file_path:
        delete_product_picture(product.image_4_file_path, product.thumb50_4_file_path, product.thumb100_4_file_path, product.thumb270_4_file_path)
    if product.image_5_file_path:
        delete_product_picture(product.image_5_file_path, product.thumb50_5_file_path, product.thumb100_5_file_path, product.thumb270_5_file_path)

    db.session.delete(product)
    db.session.commit()
    flash('Товар удален из базы', 'success')
    return redirect(url_for('products.product_list'))


@products.route("/copy_product/<int:product_id>", methods=['POST'])
@login_required
def copy_product(product_id):
    old_product = Product.query.get_or_404(product_id)
    colors = Color.query.all()
    materials = Material.query.all()
    chipsizes = Chipsize.query.all()
    surfaces = Surface.query.all()
    uses = Use.query.all()

    print(old_product.colors)

    new_product = Product(category=Category.query.get(old_product.category.id),
                          brand=Brand.query.get(old_product.brand.id),
                          name="Копия " + old_product.name,
                          subname=old_product.subname,
                          price=old_product.price,
                          discount=old_product.discount,
                          price_currency=old_product.price_currency,
                          price_unit=old_product.price_unit,
                          description=old_product.description,
                          length_mm=old_product.length_mm,
                          width_mm=old_product.width_mm,
                          height_mm=old_product.height_mm,
                          weight_kg=old_product.weight_kg,
                          active=False,
                          popular=False)

    for color in colors:
        if color in old_product.colors:
            new_product.colors.append(color)

    for material in materials:
        if material in old_product.materials:
            new_product.materials.append(material)

    for chipsize in chipsizes:
        if chipsize in old_product.chipsizes:
            new_product.chipsizes.append(chipsize)

    for surface in surfaces:
        if surface in old_product.surfaces:
            new_product.surfaces.append(surface)

    for use in uses:
        if use in old_product.uses:
            new_product.uses.append(use)

    db.session.add(new_product)
    db.session.commit()
    flash('Данные товара скопированы (кроме картинок)', 'success')
    products_qty = Product.query.count()
    last_page = int(products_qty / products_per_page) + 1
    #print('Last page ' + str(last_page))

    return redirect(url_for('products.product_list', page=last_page))
