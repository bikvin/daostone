from flask import (Blueprint, abort, render_template, redirect, url_for, flash, request)
from flask_login import current_user, login_required
from sqlalchemy import and_, or_

from daosite import db
from daosite.models import GroupFlag, Category
from daosite.groupflag.forms import FlagForm

groupflag = Blueprint('groupflag', __name__)



@groupflag.route("/flag/group/all/list", methods=['GET', 'POST'])
@login_required
def group_flag_list():
    if current_user.status != 'admin':
        abort(403)
    flag_items = GroupFlag.query.order_by(GroupFlag.order_id.asc())
    print(flag_items.all())
    return render_template('flag/group_flag_list.html', title='flag', flag_items=flag_items)

@groupflag.route("/flag/group/new", methods=['GET', 'POST'])
@login_required
def groupflag_new():
    # site_vars = SiteVariable.query()
    categories = Category.query.all()
    form = FlagForm()

    form.categories.choices = [(g.id, g.name) for g in categories]
    # form.site_var_id.choices = [(g.id, g.name) for g in site_vars]
    if form.validate_on_submit():

        flag_item = GroupFlag(
            title= form.title.data,
            order_id=form.order_id.data,
            active = form.active.data
            )

        for category in categories:
            if category.id in form.categories.data:
                flag_item.categories.append(category)
            else:
                if category in flag_item.categories:
                    flag_item.categories.append(category)

        db.session.add(flag_item)
        db.session.commit()

        flash('Группа для флагов создан', 'success')
        return redirect(url_for('groupflag.group_flag_list'))

    # elif request.method == 'GET':
    return render_template('flag/creategroup_flag_item.html', title='Создание группы флагов', legend='Новая группа флагов', form=form, flag=GroupFlag())

    # return render_template('content/create_content_item.html', title='Создание контента', legend='Новый контент', form=form, content=Content())
    # return redirect(url_for('content.content_list'))

@groupflag.route("/flag/group/edit", methods=['GET', 'POST'])
@groupflag.route("/flag/group/edit/<int:item_id>", methods=['GET', 'POST'])
@login_required
def groupflag_edit(item_id):
    categories = Category.query.all()
    # site_vars = SiteVariable.query
    form = FlagForm()
    # form.site_var_id.choices = [(g.id, g.name) for g in site_vars]
    form.categories.choices = [(g.id, g.name) for g in categories]

    flag_item = GroupFlag.query.get_or_404(item_id)

    if form.validate_on_submit():
        
        flag_item.title = form.title.data
        flag_item.order_id = form.order_id.data
        flag_item.active = form.active.data

        for category in categories:
            if category.id in form.categories.data:
                flag_item.categories.append(category)
            else:
                if category in flag_item.categories:
                    flag_item.categories.append(category)

        db.session.commit()

        flash('Группа флагов обновлена', 'success')
        return redirect(url_for('groupflag.group_flag_list'))

    elif request.method == 'GET':

        form.title.data = flag_item.title
        form.order_id.data = flag_item.order_id
        form.active.data = flag_item.active

        form.categories.data = [category.id for category in flag_item.categories]
        

    return render_template('flag/creategroup_flag_item.html', title='Редактирование группы флагов', legend='Редактирование группы флагов #' + str(flag_item.id), form=form, flag_item=GroupFlag())
    # return render_template('content/create_content_item.html', title='Редактирование редактирование', legend='Редактирование контента #' + str(content_item.id), form=form, content=Content())

    # return redirect(url_for('content.content_list'))

@groupflag.route("/flag/group/<int:item_id>/delete", methods=['POST'])
@login_required
def deletegroup_flag_item(item_id):
    if current_user.status != 'admin':
        abort(403)
    flag = GroupFlag.query.get_or_404(item_id)

    db.session.delete(flag)
    db.session.commit()
    flash('Группа флагов удалена из базы', 'success')
    return redirect(url_for('groupflag.group_flag_list'))

# @groupflag.context_processor
# def utility_processor():
#     def category_count(flags_group_id):
#         return 0
#     return dict(category_count=category_count)