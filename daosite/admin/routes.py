from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from daosite import db
from daosite.models import Online_order
from daosite.colors.forms import ColorForm

admin = Blueprint('admin', __name__)


@admin.route("/admin")
@login_required
def admin_dash():
    orders = Online_order.query.order_by(Online_order.id.desc())
    

    return render_template('admin/admin.html', title='Orders', orders=orders)
