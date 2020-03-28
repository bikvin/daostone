from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ColorForm(FlaskForm):
    name = StringField('Цвет', validators=[DataRequired()])
    url_name = StringField('URL название цвета', validators=[DataRequired()])
    page_title = StringField('Заголовок на странице')
    header_title = StringField('Заголовок в хедере')
    meta_description = StringField('Мета описание')
    description = TextAreaField('Описание')
    submit = SubmitField('Сохранить')
