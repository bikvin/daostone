from flask import (Blueprint, abort, render_template, redirect, url_for, flash, request)
from flask_login import current_user, login_required
from sqlalchemy import and_, or_

from daosite import db
from daosite.models import Flag, GroupFlag
from daosite.flag.forms import FlagForm

flag = Blueprint('flag', __name__)



@flag.route("/flag/list", methods=['GET', 'POST'])
# @flag.route("/flag/list/<string:item_value>", methods=['GET', 'POST'])
@login_required
def flag_list():
    # print(item_value)
    if current_user.status != 'admin':
        abort(403)
        
    # flag_filter = Flag.query.filter(Flag.grouppa == item_value)
    # print(flag_filter.all())
    flag_items = Flag.query.order_by(Flag.id.asc())
    print(flag_items.all())
    return render_template('flag/flag_list.html', title='flag', flag_items=flag_items)

@flag.route("/flag/new", methods=['GET', 'POST'])
@login_required
def new():
    # site_vars = SiteVariable.query()
    form = FlagForm()
    # form.site_var_id.choices = [(g.id, g.name) for g in site_vars]
    if form.validate_on_submit():


        name_var = form.get_var_name()
        exist_flag_binding = Flag.query.filter(Flag.name_var == name_var)
        if exist_flag_binding.count() and name_var != 'None':
                flash('Контент для %s уже существует' % name_var, 'warning')
        else:
        
            flag_item = Flag(
                gruppa= form.title.data,
                name_var=name_var,
                value = form.value.data)

            db.session.add(flag_item)
            db.session.commit()

            flash('Флаг создан', 'success')
            return redirect(url_for('flag.flag_list'))

    # elif request.method == 'GET':
    return render_template('flag/create_flag_item.html', title='Создание флага', legend='Новый флаг', form=form, flag=Flag())

    # return render_template('content/create_content_item.html', title='Создание контента', legend='Новый контент', form=form, content=Content())
    # return redirect(url_for('content.content_list'))

@flag.route("/flag/edit", methods=['GET', 'POST'])
@flag.route("/flag/edit/<int:item_id>", methods=['GET', 'POST'])
@login_required
def edit(item_id):

    # site_vars = SiteVariable.query
    form = FlagForm()
    # form.site_var_id.choices = [(g.id, g.name) for g in site_vars]
    flag_item = Flag.query.get_or_404(item_id)

    if form.validate_on_submit():
        
        name_var = form.get_var_name()
        exist_flag_binding = Flag.query.filter(Flag.name_var == name_var)
        if exist_flag_binding.count() and name_var != 'None':
                flash('Контент для %s уже существует' % name_var, 'warning')
        else:
            # flag_item.title = form.title.data
            flag_item.value = form.value.data
            flag_item.name_var = name_var
            db.session.commit()

            flash('Контент обновлен', 'success')
            return redirect(url_for('flag.flag_list'))

    elif request.method == 'GET':

        # form.title.data = flag_item.title
        form.value.data = flag_item.value
        get_var_key = form.get_var_key(flag_item.name_var)
        form.name_var.data =  get_var_key

    return render_template('flag/create_flag_item.html', title='Редактирование редактирование', legend='Редактирование флага #' + str(flag_item.id), form=form, flag=Flag())
    # return render_template('content/create_content_item.html', title='Редактирование редактирование', legend='Редактирование контента #' + str(content_item.id), form=form, content=Content())

    # return redirect(url_for('content.content_list'))

@flag.route("/flag/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_flag_item(item_id):
    if current_user.status != 'admin':
        abort(403)
    flag = Flag.query.get_or_404(item_id)


    db.session.delete(flag)
    db.session.commit()
    flash('Флаг удален из базы', 'success')
    return redirect(url_for('flag.flag_list'))