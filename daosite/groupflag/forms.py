from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

NAME_VARS = (
    ('0', 'None'),
    ('1', '@Red'),
    ('2', '@Green'),
    ('3','@Blue')
)

class FlagForm(FlaskForm):
    
    title = StringField('Имя группы', validators=[DataRequired()])
    value = TextAreaField('ключевое имя')
    name_var = SelectField('ключ', choices=NAME_VARS)

    submit = SubmitField('Сохранить')

    def get_var_name(self):
        return dict(NAME_VARS).get(self.name_var.data)

    def get_var_key(self, value):
        if value is None:
            result = '0'
        else:
            result = list(dict(NAME_VARS).keys())[list(dict(NAME_VARS).values()).index(value)]
        return result
        