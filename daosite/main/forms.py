from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Email


class OrderForm(FlaskForm):
    # delivery = SelectField('Доставка', choices=[('mkad_delivery', 'Доставка в пределах МКАД (бесплатно при сумме заказа больше &#8381 30000)'), ('self', 'Самовывоз из шоурума')])
    delivery = RadioField('Доставка', choices=[('mkad', 'Доставка в пределах МКАД (бесплатно при сумме заказа больше &#8381 30000)'), ('self', 'Самовывоз из шоурума')])
    name = StringField('Ваше имя', validators=[DataRequired("Пожалуйста укажите ваше имя.")])
    phone = StringField('Телефон для связи', validators=[DataRequired()])
    email = StringField('Электронная почта')
    address = TextAreaField('Адрес доставки')
    comment = TextAreaField('Комментарий')
    submit = SubmitField('Оформить заказ')


class SearchForm(FlaskForm):
    q = TextAreaField('Запрос поиска')

    class Meta:
        csrf = False
