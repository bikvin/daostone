from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField, SelectMultipleField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed


class InteriorForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    products = SelectMultipleField('Мозайка', choices=[], coerce=str)
    images = MultipleFileField(
        'Изображения интерьера',
        validators=[
            FileAllowed(['png', 'jpeg', 'jpg'], 'Image only!')
        ]
    )
    submit = SubmitField('Сохранить')
