from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from daosite import db
from daosite.models import Material
from daosite.materials.forms import MaterialForm

materials = Blueprint('materials', __name__)


@materials.route("/material/new", methods=['GET', 'POST'])
@login_required
def new_material():
    #if current_user.status != 'admin':
        #abort(403)
    form = MaterialForm()
    if form.validate_on_submit():

        material = Material(name=form.name.data,
                            url_name=form.url_name.data,
                            page_title=form.page_title.data,
                            header_title=form.header_title.data,
                            meta_description=form.meta_description.data,
                            description=form.description.data)
        db.session.add(material)
        db.session.commit()
        flash('Цатериал создан', 'success')
        return redirect(url_for('materials.material_list'))
    return render_template('materials/create_material.html', title='Создать материал', form=form, legend='Новый материал')


@materials.route("/material_list")
@login_required
def material_list():
    #if current_user.status != 'admin':
        #abort(403)
    materials = Material.query.all()
    return render_template('materials/material_list.html', title='Materials', materials=materials)


@materials.route("/material/<int:material_id>", methods=['GET', 'POST'])
@login_required
def edit_material(material_id):
    #if current_user.status != 'admin':
        #abort(403)
    material = Material.query.get_or_404(material_id)
    form = MaterialForm()
    if form.validate_on_submit():
        material.name = form.name.data
        material.url_name = form.url_name.data
        material.page_title = form.page_title.data
        material.header_title = form.header_title.data
        material.meta_description = form.meta_description.data
        material.description = form.description.data

        db.session.commit()
        flash('Материал обновлен', 'success')
        return redirect(url_for('materials.material_list'))
    elif request.method == 'GET':
        form.name.data = material.name
        form.url_name.data = material.url_name
        form.page_title.data = material.page_title
        form.header_title.data = material.header_title
        form.meta_description.data = material.meta_description
        form.description.data = material.description

    return render_template('materials/create_material.html', title='Редактироваие материала', form=form, legend='Редактирование материала')


@materials.route("/material/<int:material_id>/delete", methods=['POST'])
@login_required
def delete_material(material_id):
    if current_user.status != 'admin':
        abort(403)
    material = Material.query.get_or_404(material_id)
    if current_user.status != 'admin':
        abort(403)
    db.session.delete(material)
    db.session.commit()
    flash('Материал удален из базы', 'success')
    return redirect(url_for('materials.material_list'))
