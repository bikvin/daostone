from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    name = StringField('Название категории', validators=[DataRequired()])
    url_name = StringField('URL Название категории (только латинские символы)', validators=[DataRequired()])
    description = TextAreaField('Описание')
    files_directory = StringField('Директория для файлов (только латинские символы)', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
