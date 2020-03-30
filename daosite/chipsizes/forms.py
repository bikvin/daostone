from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ChipsizeForm(FlaskForm):
    name = StringField('Размер элементов', validators=[DataRequired()])
    url_name = StringField('URL-название', validators=[DataRequired()])
    page_title = StringField('Заголовок на странице')
    header_title = StringField('Заголовок в хедере')
    meta_description = StringField('Мета описание')
    description = TextAreaField('Описание')
    submit = SubmitField('Сохранить')
