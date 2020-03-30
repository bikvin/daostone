from flask import session, url_for
import math
from urllib.request import urlopen
from daosite import mail
from flask_mail import Message
import xml.etree.ElementTree as ET


def add_to_cart_session(mosaic, quantity, usd_rate, eur_rate):
    unit_price = get_unit_price(mosaic, usd_rate, eur_rate)

    new_cart_item = {
        'id': mosaic.id,
        'qty': quantity,
        'name': mosaic.name,
        'thumb_path': url_for('static', filename=mosaic.thumb100_1_file_path),
        'unit_price': unit_price,
        'category': mosaic.category.name,
        'discount': mosaic.discount
    }
    if mosaic.discount:
        new_cart_item.update({
            'price_before_discount': get_unit_price_before_discount(mosaic, usd_rate, eur_rate)
        })
    if not 'cart_items' in session:
        session['cart_items'] = []

    item_already_in_cart = False

    for cart_item in session['cart_items']:
        if cart_item['id'] == mosaic.id:
            item_already_in_cart = True
            cart_item['qty'] = cart_item['qty'] + quantity
            break

    if not item_already_in_cart:
        session['cart_items'].append(new_cart_item)
    session.modified = True
    return False


def get_unit_price(mosaic, usd_rate, eur_rate):
    price = mosaic.get_unit_actual_price

    if mosaic.price_currency == 'usd':
        price = price * usd_rate
    elif mosaic.price_currency == 'eur':
        price = price * eur_rate

    unit_price = math.floor(price)

    return unit_price


def get_unit_price_before_discount(mosaic, usd_rate, eur_rate):
    price = mosaic.get_unit_price
    
    if mosaic.price_currency == 'usd':
        price = price * usd_rate
    elif mosaic.price_currency == 'eur':
        price = price * eur_rate

    unit_price = math.floor(price)

    return unit_price


def send_user_email(email, username, order_id):
    msg = Message('Ваш заказ - daostone.ru',
                  sender='stone.dao@gmail.com',
                  recipients=email.split())
    msg.body = f'''Здравствуйте,''' + username + '''!

Ваш заказ №''' + str(order_id) + ''' получен. 

Мы скоро свяжемся с вами для подтверждения.

Спасибо!

С уважением,
DAO-красивая мозаика
www.daostone.ru
+7-985-513-27-44 

'''
    mail.send(msg)


def send_admin_email(order):
    msg = Message('Новый заказ с сайта',
                  sender='stone.dao@gmail.com',
                  recipients='stone.dao@gmail.com'.split())
    msg.body = f'''Новый заказ
Номер: ''' + str(order.id) + '''

Клиент: ''' + order.name + '''
Телефон: ''' + str(order.phone) + '''
Email: ''' + str(order.email) + '''
Адрес доставки: ''' + order.address + '''
Комментарий: ''' + order.comment + '''
Доставка: ''' + order.delivery + '''
Стоимость доставки: ''' + str(order.delivery_price) + '''р.
'''

    for item in order.ordered_items:
        msg.body += '''
''' + item.product_name + ''' - ''' + str(item.quantity) + ' шт.'
    msg.body += '''

Итого по заказу:''' + str(order.order_total) + 'р.'
    try:
        mail.send(msg)
    except:
        print("Error sending user email")


def get_rates():
    print('aaaa')
    response = urlopen('http://www.cbr-xml-daily.ru/daily_utf8.xml')
    tree = ET.parse(response)
    root = tree.getroot()
    print(root.tag)
    #usd_rate = root.find("./Valute/CharCode[.='USD']/../Value")
    #eur_rate = root.find("./Valute/CharCode[.='EUR']/../Value")
    usd_rate=root.find("./Valute[@ID='R01235']/Value")
    eur_rate=root.find("./Valute[@ID='R01239']/Value")
    #rates['USD'] = float(usd_rate.text.replace(',', '.'))
    #rates['EUR'] = float(eur_rate.text.replace(',', '.'))
    rates = {'USD': float(usd_rate.text.replace(',', '.')), 'EUR': float(eur_rate.text.replace(',', '.'))}

    return rates
