import os
import secrets
from PIL import Image
from flask import url_for, current_app
from daosite import mail
from daosite.models import User, Product


def save_product_picture(form_picture, product, image_number):
    #random_hex = secrets.token_hex(8)

    picture_directory = get_picture_directory(product)

    print('picture directory')
    print(picture_directory)
    if not os.path.exists(picture_directory):
        os.makedirs(picture_directory)

    thumb50_directory = get_thumb50_directory(picture_directory)
    thumb100_directory = get_thumb100_directory(picture_directory)
    thumb270_directory = get_thumb270_directory(picture_directory)

    if not os.path.exists(thumb50_directory):
        os.makedirs(thumb50_directory)
    if not os.path.exists(thumb100_directory):
        os.makedirs(thumb100_directory)
    if not os.path.exists(thumb270_directory):
        os.makedirs(thumb270_directory)

    picture_fn = get_picture_fn(form_picture, product, image_number)
    picture_path = get_picture_path(picture_directory, picture_fn)

    thumb50_path = get_thumbnail_path(thumb50_directory, picture_fn)
    thumb100_path = get_thumbnail_path(thumb100_directory, picture_fn)
    thumb270_path = get_thumbnail_path(thumb270_directory, picture_fn)

    output_size = (1000, 1000)
    thumb50_size = (50, 50)
    thumb100_size = (100, 100)
    thumb270_size = (270, 270)

    print(picture_path)
    picture = Image.open(form_picture)
    picture.thumbnail(output_size)
    picture.save(picture_path)

    thumb50 = Image.open(form_picture)
    thumb50.thumbnail(thumb50_size)
    thumb50.save(thumb50_path)

    thumb100 = Image.open(form_picture)
    thumb100.thumbnail(thumb100_size)
    thumb100.save(thumb100_path)

    thumb270 = Image.open(form_picture)
    thumb270.thumbnail(thumb270_size)
    thumb270.save(thumb270_path)

    picture_directory_from_static = get_picture_directory_from_static(product)
    thumb50_directory_from_static = picture_directory_from_static + "/thumb50"
    thumb100_directory_from_static = picture_directory_from_static + "/thumb100"
    thumb270_directory_from_static = picture_directory_from_static + "/thumb270"

    paths = {'image': picture_directory_from_static + '/' + picture_fn, 'thumb50': thumb50_directory_from_static + '/' + picture_fn, 'thumb100': thumb100_directory_from_static + '/' + picture_fn, 'thumb270': thumb270_directory_from_static + '/' + picture_fn}

    return paths


def delete_product_picture(image_file_path_from_static, thumb50_file_path_from_static, thumb100_file_path_from_static, thumb270_file_path_from_static):

    print(image_file_path_from_static)
    print(type(image_file_path_from_static))

    image_file_path = ''
    thumb50_file_path = ''
    thumb100_file_path = ''
    thumb270_file_path = ''

    if image_file_path_from_static:
        image_file_path = os.path.join(current_app.root_path, 'static', image_file_path_from_static)
    if thumb50_file_path_from_static:
        thumb50_file_path = os.path.join(current_app.root_path, 'static', thumb50_file_path_from_static)
    if thumb100_file_path_from_static:
        thumb100_file_path = os.path.join(current_app.root_path, 'static', thumb100_file_path_from_static)
    if thumb270_file_path_from_static:
        thumb270_file_path = os.path.join(current_app.root_path, 'static', thumb270_file_path_from_static)

    if os.path.exists(image_file_path):
        os.remove(image_file_path)
    else:
        print("Sorry, I can not remove %s file." % image_file_path)

    if os.path.exists(thumb50_file_path):
        os.remove(thumb50_file_path)
    else:
        print("Sorry, I can not remove %s file." % thumb50_file_path)

    if os.path.exists(thumb100_file_path):
        os.remove(thumb100_file_path)
    else:
        print("Sorry, I can not remove %s file." % thumb100_file_path)

    if os.path.exists(thumb270_file_path):
        os.remove(thumb270_file_path)
    else:
        print("Sorry, I can not remove %s file." % thumb270_file_path)


def get_picture_fn(form_picture, product, image_number):
    _, f_ext = os.path.splitext(form_picture.filename)
    return prepare_file_name(product.category.name) + "-" + prepare_file_name(product.name) + "-p" + str(image_number) + f_ext


def get_picture_path(picture_directory, picture_fn):
    return os.path.join(picture_directory, picture_fn)


def get_thumbnail_path(thumbnail_directory, picture_fn):
    return os.path.join(thumbnail_directory, picture_fn)


def get_picture_directory_from_static(product):
    return os.path.join('product_pics', product.category.files_directory, product.brand.files_directory)


def get_picture_directory(product):
    return os.path.join(current_app.root_path, 'static', get_picture_directory_from_static(product))


def get_thumb50_directory(picture_directory):
    return os.path.join(picture_directory, 'thumb50')


def get_thumb100_directory(picture_directory):
    return os.path.join(picture_directory, 'thumb100')


def get_thumb270_directory(picture_directory):
    return os.path.join(picture_directory, 'thumb270')


def prepare_file_name(filename):
    change_dict = {" ": "-", "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e", "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya", "!": "", "№": "", ";": "", "%": "", ":": "", "?": "", "*": "", "(": "", ")": "", "/": "", "\\": "", ".": "", ",": "", "@": "", "#": "", "$": "", "%": "", "^": "", "&": "", "*": "", "*": "", "(": "", ")": "", "/": "", "'": "", "[": "", "]": "", "{": "", "}": "", "<": "", ">": ""}

    for character in filename:

        if character in change_dict:
            # print(character)
            filename = filename.replace(character, change_dict[character])
            # print(filename)

        if character.lower() in change_dict:
            # print(character)
            filename = filename.replace(character, change_dict[character.lower()])
            # print(filename)

    return filename
