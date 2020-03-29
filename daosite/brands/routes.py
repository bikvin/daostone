from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from daosite import db
from daosite.models import Brand
from daosite.brands.forms import BrandForm

brands = Blueprint('brands', __name__)


@brands.route("/brand/new", methods=['GET', 'POST'])
@login_required
def new_brand():
    # if current_user.status != 'admin':
        # abort(403)
    form = BrandForm()
    if form.validate_on_submit():

        brand = Brand(name=form.name.data,
                      info=form.info.data,
                      files_directory=form.files_directory.data,
                      url_name=form.url_name.data,
                      page_title=form.page_title.data,
                      header_title=form.header_title.data,
                      meta_description=form.meta_description.data,
                      description=form.description.data,
                      discount=form.discount.data)
        db.session.add(brand)
        db.session.commit()
        flash('Бренд создан', 'success')
        return redirect(url_for('brands.brand_list'))
    return render_template('brands/create_brand.html', title='Создать бренд', form=form, legend='Новый бренд')


@brands.route("/brand_list")
@login_required
def brand_list():
    # if current_user.status != 'admin':
        # abort(403)
    brands = Brand.query.all()
    return render_template('brands/brand_list.html', title='Brands', brands=brands)


@brands.route("/brand/<int:brand_id>", methods=['GET', 'POST'])
@login_required
def edit_brand(brand_id):
    # if current_user.status != 'admin':
        # abort(403)
    brand = Brand.query.get_or_404(brand_id)
    form = BrandForm()
    if form.validate_on_submit():
        brand.name = form.name.data
        brand.url_name = form.url_name.data
        brand.page_title = form.page_title.data
        brand.header_title = form.header_title.data
        brand.meta_description = form.meta_description.data
        brand.description = form.description.data
        brand.info = form.info.data
        brand.files_directory = form.files_directory.data
        brand.discount=form.discount.data
        db.session.commit()
        flash('Бренд обновлен', 'success')
        return redirect(url_for('brands.brand_list'))
    elif request.method == 'GET':
        form.name.data = brand.name
        form.url_name.data = brand.url_name
        form.page_title.data = brand.page_title
        form.header_title.data = brand.header_title
        form.meta_description.data = brand.meta_description
        form.description.data = brand.description
        form.info.data = brand.info
        form.files_directory.data = brand.files_directory
        form.discount.data = brand.discount
    return render_template('brands/create_brand.html', title='Редактироваие бренда', form=form, legend='Редактирование бренда')


@brands.route("/brand/<int:brand_id>/delete", methods=['POST'])
@login_required
def delete_brand(brand_id):
    if current_user.status != 'admin':
        abort(403)
    brand = Brand.query.get_or_404(brand_id)
    if current_user.status != 'admin':
        abort(403)
    db.session.delete(brand)
    db.session.commit()
    flash('Бренд удален из базы', 'success')
    return redirect(url_for('brands.brand_list'))
