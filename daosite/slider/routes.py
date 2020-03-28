from flask import (Blueprint, abort, flash, request, redirect, render_template, url_for)
from flask_login import current_user, login_required

from daosite import db
from daosite.models import Slider
from daosite.slider.forms import SliderForm
from daosite.slider.utils import StringConverter, save_slide_picture, delete_slide_picture

slider = Blueprint('slider', __name__)

# @slider.route("/slider/new", methods=['GET', 'POST'])
# @login_required
# def new_slider_item():
#     return ''

@slider.route("/slider/list", methods=['GET', 'POST'])
@login_required
def slider_list():
    if current_user.status != 'admin':
        abort(403)
    slider_items = Slider.query.order_by(Slider.order_id.asc())
    print(slider_items.all())
    return render_template('slider/slider_list.html', title='slider', slider_items=slider_items)

@slider.route("/slider/new", methods=['GET', 'POST'])
@login_required
def new():
    form = SliderForm()

    if form.validate_on_submit():
        slider_item = Slider(
            title= form.title.data,
            description = form.description.data,
            button_title = form.button_title.data,
            button_url = form.button_url.data,
            order_id = form.order_id.data,
            active = form.active.data)

        if form.image.data:
            slider_item.image_file_path = save_slide_picture(form.image.data, slider_item)

        db.session.add(slider_item)
        db.session.commit()

        flash('Слайд создан', 'success')
        return redirect(url_for('slider.slider_list'))

    elif request.method == 'GET':
        return render_template('slider/create_slider_item.html', title='Создание слайда', legend='Новый слайд', form=form, slider=Slider())


@slider.route("/slider/edit", methods=['GET', 'POST'])
@slider.route("/slider/edit/<int:item_id>", methods=['GET', 'POST'])
@login_required
def edit(item_id):

    form = SliderForm()
    slider_item = Slider.query.get_or_404(item_id)

    if form.validate_on_submit():
    
        slider_item.title = form.title.data
        slider_item.description = form.description.data
        slider_item.button_title = form.button_title.data
        slider_item.button_url = form.button_url.data
        slider_item.order_id = form.order_id.data
        slider_item.active = form.active.data

        if form.image.data:
            slider_item.image_file_path = save_slide_picture(form.image.data, slider_item)

        if form.delete_image.data:
            delete_slide_picture(slider_item.image_file_path)
            slider_item.image_file_path = None

        db.session.commit()

        flash('Слайд обновлен', 'success')
        return redirect(url_for('slider.slider_list'))

    elif request.method == 'GET':

        form.title.data = slider_item.title
        form.description.data = slider_item.description
        form.button_title.data = slider_item.button_title
        form.button_url.data = slider_item.button_url
        form.order_id.data = slider_item.order_id
        form.image_file_path = slider_item.image_file_path
        form.active.data = slider_item.active

        return render_template('slider/create_slider_item.html', title='Редактирование слайд', legend='Редактирование слайда #' + str(slider_item.order_id), form=form, slider=Slider())


@slider.route("/slider/<int:item_id>/delete", methods=['POST'])
@login_required
def delete_slider_item(item_id):
    if current_user.status != 'admin':
        abort(403)
    slide = Slider.query.get_or_404(item_id)

    if slide.image_file_path:
        delete_slide_picture(slide.image_file_path)

    db.session.delete(slide)
    db.session.commit()
    flash('Слайд удалена из базы', 'success')
    return redirect(url_for('slider.slider_list'))

@slider.app_template_filter('short_str')
def to_short_str(value, length=20):
    return StringConverter.to_short_str(value, length)

# @slider.context_processor
# def utility_processor():
#     def to_short_str(value):
#         return StringConverter.to_short_str(value)
#     return dict(to_short_str=to_short_str)