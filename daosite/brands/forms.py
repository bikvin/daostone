from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class BrandForm(FlaskForm):
    name = StringField('Название бренда', validators=[DataRequired()])
    files_directory = StringField('Директория для файлов(только латинские буквы)', validators=[DataRequired()])
    info = TextAreaField('Информация')
    page_title = StringField('Заголовок на странице')
    header_title = StringField('Заголовок в хедере')
    meta_description = StringField('Мета описание')
    description = TextAreaField('Описание')
    submit = SubmitField('Сохранить')
    url_name = StringField('URL Название бренда (только латинские буквы)', validators=[DataRequired()])
