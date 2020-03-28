from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from daosite import db
from daosite.models import Use
from daosite.uses.forms import UseForm

uses = Blueprint('uses', __name__)


@uses.route("/use/new", methods=['GET', 'POST'])
@login_required
def new_use():
    #if current_user.status != 'admin':
        #abort(403)
    form = UseForm()
    if form.validate_on_submit():

        use = Use(name=form.name.data,
                  url_name=form.url_name.data,
                  page_title=form.page_title.data,
                  header_title=form.header_title.data,
                  meta_description=form.meta_description.data,
                  description=form.description.data)
        db.session.add(use)
        db.session.commit()
        flash('Применение создан', 'success')
        return redirect(url_for('uses.use_list'))
    return render_template('uses/create_use.html', title='Создать применение', form=form, legend='Новое применение')


@uses.route("/use_list")
@login_required
def use_list():
    #if current_user.status != 'admin':
        #abort(403)
    uses = Use.query.all()
    return render_template('uses/use_list.html', title='Uses', uses=uses)


@uses.route("/use/<int:use_id>", methods=['GET', 'POST'])
@login_required
def edit_use(use_id):
    #if current_user.status != 'admin':
        #abort(403)
    use = Use.query.get_or_404(use_id)
    form = UseForm()
    if form.validate_on_submit():
        use.name = form.name.data
        use.url_name = form.url_name.data
        use.page_title = form.page_title.data
        use.header_title = form.header_title.data
        use.meta_description = form.meta_description.data
        use.description = form.description.data
        db.session.commit()
        flash('Применение обновлено', 'success')
        return redirect(url_for('uses.use_list'))
    elif request.method == 'GET':
        form.name.data = use.name
        form.url_name.data = use.url_name
        form.page_title.data = use.page_title
        form.header_title.data = use.header_title
        form.meta_description.data = use.meta_description
        form.description.data = use.description

    return render_template('uses/create_use.html', title='Редактирование применения', form=form, legend='Редактирование применения')


@uses.route("/use/<int:use_id>/delete", methods=['POST'])
@login_required
def delete_use(use_id):
    if current_user.status != 'admin':
        abort(403)
    use = Use.query.get_or_404(use_id)
    if current_user.status != 'admin':
        abort(403)
    db.session.delete(use)
    db.session.commit()
    flash('Применение удалено из базы', 'success')
    return redirect(url_for('uses.use_list'))
