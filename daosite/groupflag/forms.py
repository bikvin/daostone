from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SelectField, SubmitField, IntegerField, BooleanField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Optional

# NAME_VARS = (
#     ('0', 'None'),
#     ('1', '@Red'),
#     ('2', '@Green'),
#     ('3','@Blue')
# )

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class FlagForm(FlaskForm):
    
    title = StringField('Имя группы', validators=[DataRequired()])
    order_id = IntegerField('Порядковый номер', validators=[Optional()])
    active = BooleanField('Опубликовано на сайте')

    categories = MultiCheckboxField('Категории', coerce=int)
    
    is_topmenu_show = BooleanField('Отображать в верхнем меню')

    submit = SubmitField('Сохранить')
        