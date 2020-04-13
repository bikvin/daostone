from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField, widgets
from wtforms.validators import DataRequired


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CategoryForm(FlaskForm):
    name = StringField('Название категории', validators=[DataRequired()])
    url_name = StringField('URL Название категории (только латинские символы)', validators=[DataRequired()])
    description = TextAreaField('Описание')
    files_directory = StringField('Директория для файлов (только латинские символы)', validators=[DataRequired()])

    group_flags = MultiCheckboxField('Группы флагов', coerce=int)

    submit = SubmitField('Сохранить')
