from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from daosite import db
from daosite.models import Category, GroupFlag
from daosite.categories.forms import CategoryForm

categories = Blueprint('categories', __name__)


@categories.route("/category/new", methods=['GET', 'POST'])
@login_required
def new_category():
    # if current_user.status != 'admin':
        # abort(403)

    group_flags = GroupFlag.query.all()

    form = CategoryForm()

    form.group_flags.choices = [(g.id, g.title) for g in group_flags]

    if form.validate_on_submit():

        category = Category(name=form.name.data,
                            description=form.description.data,
                            files_directory=form.files_directory.data,
                            url_name=form.name.data)

        for group_flag in group_flags:
            if group_flag.id in form.group_flags.data:
                category.group_flags.append(group_flag)
            else:
                if group_flag in category.group_flags:
                    category.group_flags.append(group_flag)

        db.session.add(category)
        db.session.commit()
        flash('Категория создана', 'success')
        return redirect(url_for('categories.category_list'))
    return render_template('categories/create_category.html', title='Создать категорию', form=form, legend='Новая категория')


@categories.route("/category_list")
@login_required
def category_list():
    # if current_user.status != 'admin':
        # abort(403)
    categories = Category.query.all()
    return render_template('categories/category_list.html', title='Categories', categories=categories)


@categories.route("/category/<int:category_id>", methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    # if current_user.status != 'admin':
        # abort(403)

    group_flags = GroupFlag.query.all()

    category = Category.query.get_or_404(category_id)
    form = CategoryForm()

    form.group_flags.choices = [(g.id, g.title) for g in group_flags]
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.url_name = form.url_name.data
        category.description = form.description.data
        category.files_directory = form.files_directory.data

        for group_flag in group_flags:
            if group_flag.id in form.group_flags.data:
                category.group_flag.append(group_flag)
            else:
                if group_flag in category.group_flag:
                    category.group_flag.append(group_flag)

        db.session.commit()
        flash('Категория обновлена', 'success')
        return redirect(url_for('categories.category_list'))
    elif request.method == 'GET':
        form.name.data = category.name
        form.url_name.data = category.url_name
        form.description.data = category.description
        form.files_directory.data = category.files_directory

        form.group_flags.data = [group_flag.id for group_flag in category.group_flag]

    return render_template('categories/create_category.html', title='Редактироваие категории', form=form, legend='Редактирование категории')


@categories.route("/category/<int:category_id>/delete", methods=['POST'])
@login_required
def delete_category(category_id):
    if current_user.status != 'admin':
        abort(403)
    category = Category.query.get_or_404(category_id)
    if current_user.status != 'admin':
        abort(403)
    db.session.delete(category)
    db.session.commit()
    flash('Категория удалена из базы', 'success')
    return redirect(url_for('categories.category_list'))
