from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from daosite import db
from daosite.models import Color
from daosite.colors.forms import ColorForm

colors = Blueprint('colors', __name__)


@colors.route("/color/new", methods=['GET', 'POST'])
@login_required
def new_color():
    #if current_user.status != 'admin':
        #abort(403)
    form = ColorForm()
    if form.validate_on_submit():

        color = Color(name=form.name.data,
                      url_name=form.url_name.data,
                      page_title=form.page_title.data,
                      header_title=form.header_title.data,
                      meta_description=form.meta_description.data,
                      description=form.description.data)
        db.session.add(color)
        db.session.commit()
        flash('Цвет создан', 'success')
        return redirect(url_for('colors.color_list'))
    return render_template('colors/create_color.html', title='Создать цвет', form=form, legend='Новый цвет')


@colors.route("/color_list")
@login_required
def color_list():
    #if current_user.status != 'admin':
        #abort(403)
    colors = Color.query.all()
    return render_template('colors/color_list.html', title='Colors', colors=colors)


@colors.route("/color/<int:color_id>", methods=['GET', 'POST'])
@login_required
def edit_color(color_id):
    #if current_user.status != 'admin':
        #abort(403)
    color = Color.query.get_or_404(color_id)
    form = ColorForm()
    if form.validate_on_submit():
        color.name = form.name.data
        color.url_name = form.url_name.data
        color.page_title = form.page_title.data
        color.header_title = form.header_title.data
        color.meta_description = form.meta_description.data
        color.description = form.description.data

        db.session.commit()
        flash('Цвет обновлен', 'success')
        return redirect(url_for('colors.color_list'))
    elif request.method == 'GET':
        form.name.data = color.name
        form.url_name.data = color.url_name
        form.page_title.data = color.page_title
        form.header_title.data = color.header_title
        form.meta_description.data = color.meta_description
        form.description.data = color.description

    return render_template('colors/create_color.html', title='Редактироваие цвета', form=form, legend='Редактирование цвета')


@colors.route("/color/<int:color_id>/delete", methods=['POST'])
@login_required
def delete_color(color_id):
    if current_user.status != 'admin':
        abort(403)
    color = Color.query.get_or_404(color_id)
    if current_user.status != 'admin':
        abort(403)
    db.session.delete(color)
    db.session.commit()
    flash('Цвет удален из базы', 'success')
    return redirect(url_for('colors.color_list'))
