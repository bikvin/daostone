from flask_wtf import FlaskForm
from sqlalchemy import and_
from wtforms import IntegerField, SelectMultipleField, widgets

from daosite import db
from daosite.main.utils import get_rates
from daosite.models import (Brand, Chipsize, Color, Material, Product, Rate,
                            Surface, Use, chipsize_product, color_product,
                            material_product, surface_product, use_product)


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class FilterForm(FlaskForm):
    fields_data = {
            'materials': Material,
            'manufacturers': Brand,
            'applications': Use,
            'colors': Color,
            'sizes': Chipsize,
            'surfaces': Surface
    }
    price_min = IntegerField('Минимальная цена')
    price_max = IntegerField('Максимальная цена')
    materials = MultiCheckboxField('Материал', choices=[], coerce=int,)
    manufacturers = MultiCheckboxField('Производитель', choices=[], coerce=int,)
    applications = MultiCheckboxField('Применение', choices=[], coerce=int,)
    colors = MultiCheckboxField('Цвет', choices=[], coerce=int,)
    sizes = MultiCheckboxField('Размер', choices=[], coerce=int,)
    surfaces = MultiCheckboxField('Поверхность', choices=[], coerce=int,)

    class Meta:
        csrf = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usd_rate = Rate.query.filter(Rate.name == 'usd').first().value
        self.eur_rate = Rate.query.filter(Rate.name == 'eur').first().value
        self._get_price_range()
        self.create_chloices()

    def _get_price_range(self, *args):
        query = Product.query.filter(Product.active == True)
        if not self.price_min.data and not self.price_max.data:
            rur_prices = [
                product.get_m2_actual_price for product in query.filter(Product.price_currency == 'rur')
            ]
            usd_prices = [
                product.get_m2_actual_price * self.usd_rate for product in query.filter(Product.price_currency == 'usd')
            ]
            eur_prices = [
                product.get_m2_actual_price * self.eur_rate for product in query.filter(Product.price_currency == 'eur')
            ]
            prices = rur_prices + usd_prices + eur_prices
            self.price_min.data = int(min(prices))
            self.price_max.data = int(max(prices)) + 100

    def create_choices_from_model(self, field_name, model):
        items = model.query.filter().all()
        choices = [
            (item.id, item.name) for item in items
        ]
        field = getattr(self, field_name)
        field.choices = choices

    def create_chloices(self):
        for field_name, model in self.fields_data.items():
            self.create_choices_from_model(field_name, model)

    def filter_query(self, query):
        if self.price_min.data and self.price_max.data:
            price_min = self.price_min.data
            price_max = self.price_max.data

            rur_query = query.filter(Product.price_currency == 'rur')
            usd_query = query.filter(Product.price_currency == 'usd')
            eur_query = query.filter(Product.price_currency == 'eur')

            usd_prices = [price_min / self.usd_rate, price_max / self.usd_rate]
            eur_prices = [price_min / self.eur_rate, price_max / self.eur_rate]

            rur_m2_ids = [
                product.id for product in rur_query if price_min <= product.get_m2_actual_price <= price_max
            ]

            usd_m2_ids = [
                product.id for product in usd_query if usd_prices[0] <= product.get_m2_actual_price <= usd_prices[1]
            ]

            eur_m2_ids = [
                product.id for product in eur_query if eur_prices[0] <= product.get_m2_actual_price <= eur_prices[1]
            ]

            all_ids = rur_m2_ids + usd_m2_ids + eur_m2_ids
            query = query.filter(Product.id.in_(all_ids))

        if self.materials.data:
            query = query.join(material_product).filter(
                material_product.columns.material_id.in_(self.materials.data)
            )
        if self.manufacturers.data:
            query = query.join(Brand).filter(
                Brand.id.in_(self.manufacturers.data)
            )
        if self.applications.data:
            query = query.join(use_product).filter(
                use_product.columns.use_id.in_(self.applications.data)
            )
        if self.colors.data:
            query = query.join(color_product).filter(
                color_product.columns.color_id.in_(self.colors.data)
            )
        if self.sizes.data:
            query = query.join(chipsize_product).filter(
                chipsize_product.columns.chipsize_id.in_(self.sizes.data)
            )
        if self.surfaces.data:
            query = query.join(surface_product).filter(
                surface_product.columns.surface_id.in_(self.surfaces.data)
            )
        return query
