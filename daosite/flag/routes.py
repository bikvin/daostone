from flask import (Blueprint, abort, render_template, redirect, url_for, flash, request)
from flask_login import current_user, login_required
from sqlalchemy import and_, or_

from daosite import db
from daosite.models import Flag, GroupFlag
from daosite.flag.forms import FlagForm

flag = Blueprint('flag', __name__)



@flag.route("/flag/list", defaults={'flag_group_id': None}, methods=['GET', 'POST'])
@flag.route("/flag/list/<int:flag_group_id>", methods=['GET', 'POST'])
@login_required
def flag_list(flag_group_id):
    # print(item_value)
    if current_user.status != 'admin':
        abort(403)

    flag_items = None;

    # if flag_group_id == None:
    #     flag_items = Flag.query.order_by(Flag.id.asc())
    # else:
    flag_items = Flag.query.filter(Flag.group_flag_id == flag_group_id).order_by(Flag.order_id.asc())

    # flag_filter = Flag.query.filter(Flag.grouppa == item_value)
    # print(flag_filter.all())
    # flag_items = Flag.query.order_by(Flag.id.asc())
    print(flag_items.all())
    return render_template('flag/flag_list.html', title='flag', flag_items=flag_items, flag_group_id=flag_group_id)

@flag.route("/flag/new", defaults={'flag_group_id': None}, methods=['GET', 'POST'])
@flag.route("/flag/new/<int:flag_group_id>", methods=['GET', 'POST'])
@login_required
def new(flag_group_id):
    # site_vars = SiteVariable.query()
    flag_groups = GroupFlag.query.all()
    form = FlagForm()

    form.group_flag_id.choices = [(g.id, g.name) for g in flag_groups]
    # form.site_var_id.choices = [(g.id, g.name) for g in site_vars]
    if form.validate_on_submit():

        flag_item = Flag(
            name= form.name.data,
            url_name= form.url_name.data,
            order_id = form.order_id.data,
            active = form.active.data,            
            group_flag_id = form.group_flag_id.data)

        db.session.add(flag_item)
        db.session.commit()

        flash('Флаг создан', 'success')
        return redirect(url_for('flag.flag_list', flag_group_id = flag_item.group_flag_id))

    elif request.method == 'GET':
        form.group_flag_id.data = flag_group_id

    return render_template('flag/create_flag_item.html', title='Создание флага', legend='Новый флаг', form=form, flag=Flag())

    # return render_template('content/create_content_item.html', title='Создание контента', legend='Новый контент', form=form, content=Content())
    # return redirect(url_for('content.content_list'))

@flag.route("/flag/edit", methods=['GET', 'POST'])
@flag.route("/flag/edit/<int:item_id>", methods=['GET', 'POST'])
@login_required
def edit(item_id):
    flag_groups = GroupFlag.query.all()
    # site_vars = SiteVariable.query
    form = FlagForm()
    # form.site_var_id.choices = [(g.id, g.name) for g in site_vars]
    form.group_flag_id.choices = [(g.id, g.name) for g in flag_groups]
    flag_item = Flag.query.get_or_404(item_id)

    if form.validate_on_submit():
        
        flag_item.name = form.name.data
        flag_item.url_name = form.url_name.data
        flag_item.order_id = form.order_id.data
        flag_item.active = form.active.data
        flag_item.group_flag_id = form.group_flag_id.data
        db.session.commit()

        flash('Флаг обновлен', 'success')
        return redirect(url_for('flag.flag_list',flag_group_id = flag_item.group_flag_id))

    elif request.method == 'GET':

        form.name.data = flag_item.name
        form.url_name.data = flag_item.url_name
        form.order_id.data = flag_item.order_id
        form.active.data = flag_item.active
        form.group_flag_id.data = flag_item.group_flag_id

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
    return redirect(url_for('flag.flag_list',flag_group_id = flag.group_flag_id))