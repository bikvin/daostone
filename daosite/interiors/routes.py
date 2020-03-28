from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from daosite import db
from daosite.models import Interior, InteriorImage, Product
from daosite.interiors.forms import InteriorForm
from daosite.interiors.utils import save_interior_images


interiors = Blueprint('interiors', __name__)

interiors_per_page = 10


@interiors.route("/interior/new", methods=['GET', 'POST'])
@login_required
def new_interior():
#    if current_user.status != 'admin':
#        abort(403)

    form = InteriorForm()
    form.products.choices = [(str(product.id), product.name) for product in Product.query.all()]

    if form.validate_on_submit():
        interior = Interior(
            name=form.name.data,
            description=form.description.data
        )
        products = Product.query.filter(Product.id.in_(form.products.data))
        for product in products:
            interior.products.append(product)
        db.session.add(interior)
        db.session.commit()

        save_interior_images(form.images.data, interior)
        flash('Интерьер создан', 'success')
        return redirect(url_for('interiors.interior_list'))
    return render_template(
        'interiors/interior_form.html',
        title='Создать интерьер',
        form=form,
        legend='Новый интерьер',
        interior=Interior()
    )


@interiors.route("/interior_list")
@login_required
def interior_list():
    page = request.args.get('page', 1, type=int)
    interiors = Interior.query.order_by(Interior.id.asc()).paginate(page=page, per_page=interiors_per_page)
    return render_template('interiors/interior_list.html', title='interiors', interiors=interiors)


@interiors.route("/edit_interior/<int:interior_id>", methods=['GET', 'POST'])
@login_required
def edit_interior(interior_id):
    interior = Interior.query.get_or_404(interior_id)
    form = InteriorForm(obj=interior)
    form.products.choices = [(str(product.id), product.name) for product in Product.query.all()]

    if form.validate_on_submit():
        interior.name = form.name.data
        interior.description = form.description.data
        db.session.commit()
        products = Product.query.filter(Product.id.in_(form.products.data))

        for product in interior.products:
            interior.products.remove(product)
            db.session.commit()

        for product in products:
            interior.products.append(product)
            db.session.commit()
            
        if request.files['images'].filename != '':
            save_interior_images(form.images.data, interior)
        flash('Товар обновлен', 'success')

        return redirect(url_for('interiors.interior_list'))

    form.products.data = [str(product.id) for product in interior.products]
    form.images.data = [image.path for image in interior.images]
    return render_template(
        'interiors/interior_form.html',
        title='Редактирование интерьера',
        form=form,
        legend='Редактирование товара',
        interior=interior
    )


@interiors.route("/interior/<int:interior_id>/image/<int:image_id>/delete", methods=['POST'])
@login_required
def delete_image(interior_id, image_id):
#    if current_user.status != 'admin':
#        abort(403)
    interior_image = InteriorImage.query.get_or_404(image_id)

    db.session.delete(interior_image)
    db.session.commit()
    flash('Изображение удалено', 'success')
    return redirect(url_for('interiors.edit_interior', interior_id=interior_id))


@interiors.route("/interior/<int:interior_id>/delete", methods=['POST'])
@login_required
def delete_interior(interior_id):
    if current_user.status != 'admin':
        abort(403)
    interior = Interior.query.get_or_404(interior_id)
    interior.images = []
    interior.products = []
    db.session.commit()
    db.session.delete(interior)
    db.session.commit()
    flash('Интерьер удален из базы', 'success')
    return redirect(url_for('interiors.interior_list'))
