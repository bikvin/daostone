from flask_wtf import FlaskForm

from wtforms import SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired


CURRENCIES = (
    ('0', 'usd'),
    ("1", 'eur')
)


class RateForm(FlaskForm):
    name = SelectField(
        'Валюта',
        choices=CURRENCIES,
        validators=[DataRequired()]
    )
    value = FloatField('Цена валюты в рублях', validators=[DataRequired()])
    submit = SubmitField('Сохранить')

    def get_name(self):
        return dict(CURRENCIES).get(self.name.data)


class ChangeRateValueForm(FlaskForm):
    value = FloatField('Цена валюты в рублях', validators=[DataRequired()])
    submit = SubmitField('Сохранить')