import requests

from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required

from daosite import db
from daosite.models import Rate
from daosite.rates.forms import RateForm, ChangeRateValueForm
from xml.etree import ElementTree

rates = Blueprint('rates', __name__)


@rates.route("/rates/new", methods=['GET', 'POST'])
@login_required
def new_rate():
    if current_user.status != 'admin':
        abort(403)
    form = RateForm()
    if form.validate_on_submit():
        print(form.get_name())
        rate_name = form.get_name()
        exist_rates = Rate.query.filter(Rate.name == rate_name)
        if exist_rates.count():
            flash('Валюта %s уже существует' % rate_name, 'warning')
        else:
            rate = Rate(
                name=rate_name,
                value=form.value.data
            )
            db.session.add(rate)
            db.session.commit()
            flash('Валюта создана', 'success')
            return redirect(url_for('rates.rates_list'))
    return render_template(
        'rates/rates_new.html',
        title='Добавить валюту',
        form=form,
        legend='Добавить валюту',
        rate=Rate()
    )


@rates.route("/rates/list", methods=['GET', 'POST'])
@login_required
def rates_list():
    if current_user.status != 'admin':
        abort(403)
    rates = Rate.query.order_by(Rate.id.asc())
    print(rates.all())
    return render_template('rates/rates_list.html', title='rates', rates=rates)


@rates.route("/rates/edit/<int:rate_id>", methods=['GET', 'POST'])
@login_required
def edit_rate(rate_id):
    if current_user.status != 'admin':
        abort(403)
    rate = Rate.query.get_or_404(rate_id)
    form = ChangeRateValueForm(obj=rate)

    if form.validate_on_submit():
        rate.value = form.value.data
        db.session.commit()
        flash('Валюта обновлена', 'success')
        return redirect(url_for('rates.rates_list'))
    return render_template(
        'rates/rates_edit.html',
        title='Редактировать валюту',
        form=form,
        legend='Редактировать валюту',
        rate=rate
    )


@rates.route("/rates/<int:rate_id>/delete", methods=['POST'])
@login_required
def delete_rate(rate_id):
    if current_user.status != 'admin':
        abort(403)
    rate = Rate.query.get_or_404(rate_id)

    db.session.delete(rate)
    db.session.commit()
    flash('Валюта удалена из базы', 'success')
    return redirect(url_for('rates.rates_list'))


@rates.route("/rates/tasks/update_rates", methods=['GET'])
def update_rates():
    url = 'http://www.cbr-xml-daily.ru/daily_utf8.xml'
    resp = requests.get(url)
    if resp.status_code != 200:
        resp = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
        if resp.status_code != 200:
            return None
    tree = ElementTree.fromstring(resp.content)
    usd = tree.find("./Valute[@ID='R01235']/Value").text.replace(',', '.')
    eur = tree.find("./Valute[@ID='R01239']/Value").text.replace(',', '.')
    usd_rate = Rate.query.filter(Rate.name == 'usd').first()
    eur_rate = Rate.query.filter(Rate.name == 'eur').first()
    if usd_rate:
        usd_rate.value = float(usd)
    if eur_rate:
        eur_rate.value = float(eur)
    db.session.commit()
    return {'usd': usd, 'eur': eur}
