from flask_wtf import FlaskForm

from wtforms import StringField, BooleanField, TextAreaField, IntegerField, FileField, SubmitField
from wtforms.validators import DataRequired, Optional

class SliderForm(FlaskForm):
    title = StringField('Наименование', validators=[DataRequired()])
    description = TextAreaField('Описание')
    button_title = StringField('Текст кнопки', validators=[DataRequired()])
    button_url = StringField('Url кнопки', validators=[DataRequired()])
    order_id = IntegerField('Порядковый номер', validators=[Optional()])
    image = FileField('Фото')
    delete_image = BooleanField('Удалить:')
    active = BooleanField('Опубликовано на сайте')
    image_file_path = None
    submit = SubmitField('Сохранить')

    # def get_name(self):
    #     return dict(CURRENCIES).get(self.name.data)