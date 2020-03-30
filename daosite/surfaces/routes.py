from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from daosite import db
from daosite.models import Surface
from daosite.surfaces.forms import SurfaceForm

surfaces = Blueprint('surfaces', __name__)


@surfaces.route("/surface/new", methods=['GET', 'POST'])
@login_required
def new_surface():
    #if current_user.status != 'admin':
        #abort(403)
    form = SurfaceForm()
    if form.validate_on_submit():

        surface = Surface(name=form.name.data,
                          url_name=form.url_name.data,
                          page_title=form.page_title.data,
                          header_title=form.header_title.data,
                          meta_description=form.meta_description.data,
                          description=form.description.data)
        db.session.add(surface)
        db.session.commit()
        flash('Поверхность создана', 'success')
        return redirect(url_for('surfaces.surface_list'))
    return render_template('surfaces/create_surface.html', title='Создать поверхность', form=form, legend='Новая поверхность')


@surfaces.route("/surface_list")
@login_required
def surface_list():
    #if current_user.status != 'admin':
        #abort(403)
    surfaces = Surface.query.all()
    return render_template('surfaces/surface_list.html', title='Surfaces', surfaces=surfaces)


@surfaces.route("/surface/<int:surface_id>", methods=['GET', 'POST'])
@login_required
def edit_surface(surface_id):
    #if current_user.status != 'admin':
        #abort(403)
    surface = Surface.query.get_or_404(surface_id)
    form = SurfaceForm()
    if form.validate_on_submit():
        surface.name = form.name.data
        surface.url_name = form.url_name.data
        surface.page_title = form.page_title.data
        surface.header_title = form.header_title.data
        surface.meta_description = form.meta_description.data
        surface.description = form.description.data
        db.session.commit()
        flash('Поверхность обновлена', 'success')
        return redirect(url_for('surfaces.surface_list'))
    elif request.method == 'GET':
        form.name.data = surface.name
        form.url_name.data = surface.url_name
        form.page_title.data = surface.page_title
        form.header_title.data = surface.header_title
        form.meta_description.data = surface.meta_description
        form.description.data = surface.description

    return render_template('surfaces/create_surface.html', title='Редактирование поверхности', form=form, legend='Редактирование поверхности')


@surfaces.route("/surface/<int:surface_id>/delete", methods=['POST'])
@login_required
def delete_surface(surface_id):
    if current_user.status != 'admin':
        abort(403)
    surface = Surface.query.get_or_404(surface_id)
    if current_user.status != 'admin':
        abort(403)
    db.session.delete(surface)
    db.session.commit()
    flash('Поверхность удалена из базы', 'success')
    return redirect(url_for('surfaces.surface_list'))
