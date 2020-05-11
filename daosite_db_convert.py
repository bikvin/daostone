from daosite import db
from daosite import create_app
from flask_script import Manager

from daosite.models import (Brand, Category, Color, Material,
                            Product, Use, GroupFlag, Flag, Chipsize, Surface)

app = create_app()
manager = Manager(app)

debug = False

@manager.command
def hello():
    # slider = Slider.query.filter(Slider.active == True).order_by(Slider.order_id.asc())
    print('hello')

def get_next_order_id(order_id):
    order_id_max = db.session.query(db.func.max(order_id)).scalar()

    if not order_id_max:
        order_id_max = 1
    else:
        order_id_max += 1

    return order_id_max


def add_new_flag_group(flag_group_name):

    new_flag_group = GroupFlag(name= flag_group_name,
        order_id=get_next_order_id(GroupFlag.order_id),
        active = 1,
        is_topmenu_show = 1
        )

    db.session.add(new_flag_group)
    # db.session.commit()

    return new_flag_group

def group_flag_to_categories(flag_group):
    
    categories = Category.query.all()

    for category in categories:
        flag_group.categories.append(category)

    # db.session.add(flag_group)
    # db.session.commit()

def add_new_flag(entity, flag_group):
    
    new_flag = Flag(name= entity.name,
        url_name=entity.url_name,
        order_id=get_next_order_id(Flag.order_id),
        active = 1,
        group_flag_id = flag_group.id
        )

    db.session.add(new_flag)
    # db.session.commit()

    return new_flag

def add_new_flags(flag_group, entities):

    for entity in entities:
        new_flag = add_new_flag(entity,flag_group)

        if flag_group.name == 'Цвет':
            new_flag.products = entity.products
        elif flag_group.name == 'Материал':
            new_flag.products = entity.materials
        elif flag_group.name == 'Применение':
            new_flag.products = entity.uses
        elif flag_group.name == 'Размер элементов':
            new_flag.products = entity.chipsizes
        elif flag_group.name == 'Поверхность':
            new_flag.products = entity.surfaces

        db.session.commit()

def generate_group(flag_group_name):
    new_flag_group = add_new_flag_group(flag_group_name)
    group_flag_to_categories(new_flag_group)
    db.session.commit()

    return new_flag_group

def generate_flags(flag_group, entities):
    add_new_flags(flag_group, entities)
    db.session.commit()

def convert(flag_group_name, entities):
    new_flag_group = generate_group(flag_group_name)

    generate_flags(new_flag_group, entities)
    print(flag_group_name + " (" + str(new_flag_group.id) + ") " + " converted")

    # downgrade
    if debug:
        delete_flag_group(new_flag_group)

    return new_flag_group

def delete_flag_group(flag_group):
    db.session.delete(flag_group)
    db.session.commit()
    print(flag_group.name + " deleted")

@manager.command
def color(flag_group_name='Цвет'):

    new_flag_group = convert(flag_group_name, Color.query.all())

@manager.command
def material(flag_group_name='Материал'):

    new_flag_group = convert(flag_group_name, Material.query.all())

@manager.command
def use(flag_group_name='Применение'):

    new_flag_group = convert(flag_group_name, Use.query.all())

@manager.command
def chipsize(flag_group_name='Размер элементов'):

    new_flag_group = convert(flag_group_name, Chipsize.query.all())

@manager.command
def surface(flag_group_name='Поверхность'):

    new_flag_group = convert(flag_group_name, Surface.query.all())

@manager.command
def full_convert():
    color()
    material()
    use()
    chipsize()
    surface()

@manager.command
def downgrade(flag_group_id):
    print(flag_group_id + " downgrade")
    flag_group = GroupFlag.query.filter(GroupFlag.id == flag_group_id).first()
    if flag_group:
        delete_flag_group(flag_group)
        

if __name__ == "__main__":
    manager.run()