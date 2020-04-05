from flask import (Blueprint, abort, render_template, redirect, url_for, flash, request)
from flask_login import current_user, login_required
from sqlalchemy import and_, or_

from daosite import db
from daosite.models import Content
from daosite.content.forms import ContentForm

content = Blueprint('content', __name__)



@content.route("/content/list", methods=['GET', 'POST'])
@login_required
def content_list():
    if current_user.status != 'admin':
        abort(403)
    content_items = Content.query.order_by(Content.id.asc())
    print(content_items.all())
    return render_template('content/content_list.html', title='content', content_items=content_items)

@content.route("/content/new", methods=['GET', 'POST'])
@login_required
def new():
    # site_vars = SiteVariable.query()
    form = ContentForm()
    # form.site_var_id.choices = [(g.id, g.name) for g in site_vars]
    if form.validate_on_submit():


        site_var_name = form.get_site_var_name()
        exist_content_binding = Content.query.filter(Content.site_var == site_var_name)
        if exist_content_binding.count() and site_var_name != 'None':
                flash('Контент для %s уже существует' % site_var_name, 'warning')
        else:
        
            content_item = Content(
                site_var=site_var_name,
                title= form.title.data,
                value = form.value.data)

            db.session.add(content_item)
            db.session.commit()

            flash('Контент создан', 'success')
            return redirect(url_for('content.content_list'))

    # elif request.method == 'GET':
    return render_template('content/create_content_item.html', title='Создание контента', legend='Новый контент', form=form, content=Content())

    # return render_template('content/create_content_item.html', title='Создание контента', legend='Новый контент', form=form, content=Content())
    # return redirect(url_for('content.content_list'))

@content.route("/content/edit", methods=['GET', 'POST'])
@content.route("/content/edit/<int:item_id>", methods=['GET', 'POST'])
@login_required
def edit(item_id):

    # site_vars = SiteVariable.query
    form = ContentForm()
    # form.site_var_id.choices = [(g.id, g.name) for g in site_vars]
    content_item = Content.query.get_or_404(item_id)

    if form.validate_on_submit():
        
        site_var_name = form.get_site_var_name()
        exist_content_binding = Content.query.filter(Content.site_var == site_var_name)
        if exist_content_binding.count() and site_var_name != 'None':
                flash('Контент для %s уже существует' % site_var_name, 'warning')
        else:
            content_item.title = form.title.data
            content_item.value = form.value.data
            content_item.site_var = site_var_name
            db.session.commit()

            flash('Контент обновлен', 'success')
            return redirect(url_for('content.content_list'))

    elif request.method == 'GET':

        form.title.data = content_item.title
        form.value.data = content_item.value
        site_var_key = form.get_site_var_key(content_item.site_var)
        form.site_var.data =  site_var_key

    return render_template('content/create_content_item.html', title='Редактирование редактирование', legend='Редактирование контента #' + str(content_item.id), form=form, content=Content())
    # return render_template('content/create_content_item.html', title='Редактирование редактирование', legend='Редактирование контента #' + str(content_item.id), form=form, content=Content())

    # return redirect(url_for('content.content_list'))

@content.route("/content/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_content_item(item_id):
    if current_user.status != 'admin':
        abort(403)
    content = Content.query.get_or_404(item_id)


    db.session.delete(content)
    db.session.commit()
    flash('Контент удален из базы', 'success')
    return redirect(url_for('content.content_list'))