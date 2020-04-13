from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DecimalField, SelectField, BooleanField, FileField, IntegerField, FloatField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileField, FileAllowed
from daosite.models import Brand, Category


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ProductForm(FlaskForm):
    #brand = StringField('Бренд', validators=[DataRequired()])
    category_id = SelectField('Категория', coerce=int)
    brand_id = SelectField('Бренд', coerce=int)
    name = StringField('Название', validators=[DataRequired()])
    subname = StringField('Дополнительное название')
    price = DecimalField('Цена', validators=[DataRequired()])
    discount = DecimalField('Скидка в %')
    price_currency = SelectField('Валюта цены', choices=[('usd', 'доллар'), ('rur', 'рубль'), ('eur', 'евро')])
    price_unit = SelectField('Единица измерения', choices=[('m2', 'м2'), ('unit', 'штука')])
    description = TextAreaField('Описание')
    image1 = FileField('Фото 1')
    image2 = FileField('Фото 2')
    image3 = FileField('Фото 3')
    image4 = FileField('Фото 4')
    image5 = FileField('Фото 5')

    delete_image_1 = BooleanField('Удалить:')
    delete_image_2 = BooleanField('Удалить:')
    delete_image_3 = BooleanField('Удалить:')
    delete_image_4 = BooleanField('Удалить:')
    delete_image_5 = BooleanField('Удалить:')

    width_mm = IntegerField('Ширина (мм)', validators=[Optional()])
    length_mm = IntegerField('Длина (мм)', validators=[Optional()])
    height_mm = IntegerField('Толщина (мм)', validators=[Optional()])

    weight_kg = FloatField('Вес (кг)', validators=[Optional()])

    colors = MultiCheckboxField('Цвета', coerce=int)
    uses = MultiCheckboxField('Применение', coerce=int)
    surfaces = MultiCheckboxField('Поверхность', coerce=int)
    chipsizes = MultiCheckboxField('Размер элементов', coerce=int)
    materials = MultiCheckboxField('Материалы', coerce=int)

    popular = BooleanField('Отображается как популярное')
    active = BooleanField('Опубликовано на сайте')

    flags = MultiCheckboxField('Флаги', coerce=int)

    submit = SubmitField('Сохранить')
