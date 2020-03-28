from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from daosite import db
from daosite.models import Chipsize
from daosite.chipsizes.forms import ChipsizeForm

chipsizes = Blueprint('chipsizes', __name__)


@chipsizes.route("/chipsize/new", methods=['GET', 'POST'])
@login_required
def new_chipsize():
    # if current_user.status != 'admin':
        # abort(403)
    form = ChipsizeForm()
    if form.validate_on_submit():

        chipsize = Chipsize(name=form.name.data,
                            url_name=form.url_name.data,
                            page_title=form.page_title.data,
                            header_title=form.header_title.data,
                            meta_description=form.meta_description.data,
                            description=form.description.data)
        db.session.add(chipsize)
        db.session.commit()
        flash('Размер элементов создан', 'success')
        return redirect(url_for('chipsizes.chipsize_list'))
    return render_template('chipsizes/create_chipsize.html', title='Создать размер элементов', form=form, legend='Новый размер элементов')


@chipsizes.route("/chipsize_list")
@login_required
def chipsize_list():
    # if current_user.status != 'admin':
        # abort(403)
    chipsizes = Chipsize.query.all()
    return render_template('chipsizes/chipsize_list.html', title='Chipsizes', chipsizes=chipsizes)


@chipsizes.route("/chipsize/<int:chipsize_id>", methods=['GET', 'POST'])
@login_required
def edit_chipsize(chipsize_id):
    # if current_user.status != 'admin':
        # abort(403)
    chipsize = Chipsize.query.get_or_404(chipsize_id)
    form = ChipsizeForm()
    if form.validate_on_submit():
        chipsize.name = form.name.data
        chipsize.url_name = form.url_name.data
        chipsize.page_title = form.page_title.data
        chipsize.header_title = form.header_title.data
        chipsize.meta_description = form.meta_description.data
        chipsize.description = form.description.data
        db.session.commit()
        flash('Цвет обновлен', 'success')
        return redirect(url_for('chipsizes.chipsize_list'))
    elif request.method == 'GET':
        form.name.data = chipsize.name
        form.url_name.data = chipsize.url_name
        form.page_title.data = chipsize.page_title
        form.header_title.data = chipsize.header_title
        form.meta_description.data = chipsize.meta_description
        form.description.data = chipsize.description

    return render_template('chipsizes/create_chipsize.html', title='Редактироваие размера элементов', form=form, legend='Редактирование размера элементов')


@chipsizes.route("/chipsize/<int:chipsize_id>/delete", methods=['POST'])
@login_required
def delete_chipsize(chipsize_id):
    if current_user.status != 'admin':
        abort(403)
    chipsize = Chipsize.query.get_or_404(chipsize_id)
    if current_user.status != 'admin':
        abort(403)
    db.session.delete(chipsize)
    db.session.commit()
    flash('Цвет удален из базы', 'success')
    return redirect(url_for('chipsizes.chipsize_list'))
