from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

SITE_VARS = (
    ('0', 'None'),
    ('1', '@AboutContent'),
    ('2', '@ContactsContent'),
    ('3','@DeliveryContent')
)

class ContentForm(FlaskForm):
    
    title = StringField('Наименование', validators=[DataRequired()])
    value = TextAreaField('Контент')
    site_var = SelectField('Переменная сайта', choices=SITE_VARS)

    submit = SubmitField('Сохранить')

    def get_site_var_name(self):
        return dict(SITE_VARS).get(self.site_var.data)

    def get_site_var_key(self, value):
        if value is None:
            result = '0'
        else:
            result = list(dict(SITE_VARS).keys())[list(dict(SITE_VARS).values()).index(value)]
        return result
        