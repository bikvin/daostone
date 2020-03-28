import re
import os
import uuid
from PIL import Image
from werkzeug.routing import BaseConverter
from flask import url_for, current_app
from daosite.models import Slider

class StringConverter(BaseConverter):

    @staticmethod
    def to_short_str(value, length=20):
       
        p = re.compile(r'^(.{%s}).*'%length)
        
        m = p.search(value)
        if m:
            return m.group(1) + '...'
        else:
            return value

def save_slide_picture(form_picture, slide):
    picture_directory = get_picture_directory(slide)

    print('picture directory')
    print(picture_directory)

    if not os.path.exists(picture_directory):
        os.makedirs(picture_directory)

    picture_fn = get_picture_fn(form_picture, slide.title)
    picture_path = get_picture_path(picture_directory, picture_fn)

    print(picture_path)
    picture = Image.open(form_picture)
    # picture.thumbnail(output_size)
    picture.save(picture_path)

    picture_directory_from_static = get_picture_directory_from_static(slide)

    return picture_directory_from_static + '/' + picture_fn

def delete_slide_picture(image_file_path_from_static):
    
    print(image_file_path_from_static)
    print(type(image_file_path_from_static))

    image_file_path = ''

    if image_file_path_from_static:
        image_file_path = '/'.join([current_app.root_path, 'static', image_file_path_from_static])

        if os.path.exists(image_file_path):
            os.remove(image_file_path)
    else:
        print("Sorry, I can not remove %s file." % image_file_path)

def get_picture_path(picture_directory, picture_fn):
    return '/'.join([picture_directory, picture_fn])

def get_picture_directory_from_static(slide):
    return '/'.join(['slider_pics'])

def get_picture_directory(slide):
    return '/'.join([current_app.root_path, 'static', get_picture_directory_from_static(slide)])

def get_picture_fn(form_picture, picture_text):
    _, f_ext = os.path.splitext(form_picture.filename)
    return prepare_file_name(picture_text) + "-sl-" + str(uuid.uuid4()) + f_ext

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