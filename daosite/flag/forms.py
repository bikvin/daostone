from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SelectField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Optional

# NAME_VARS = (
#     ('0', 'None'),
#     ('1', '@Red'),
#     ('2', '@Green'),
#     ('3','@Blue')
# )

class FlagForm(FlaskForm):
    
    # title = StringField('Группа', validators=[DataRequired()])
    # value = TextAreaField('Значение')
    # name_var = SelectField('Имя флага', choices=NAME_VARS)
    name = StringField('Имя флага', validators=[DataRequired()])
    url_name = StringField('URL-название', validators=[DataRequired()])
    order_id = IntegerField('Порядковый номер', validators=[DataRequired()])
    active = BooleanField('Опубликовано на сайте')

    group_flag_id = SelectField('Группа', coerce=int)

    submit = SubmitField('Сохранить')

    # def get_var_name(self):
    #     return dict(NAME_VARS).get(self.name_var.data)

    # def get_var_key(self, value):
    #     if value is None:
    #         result = '0'
    #     else:
    #         result = list(dict(NAME_VARS).keys())[list(dict(NAME_VARS).values()).index(value)]
    #     return result
        