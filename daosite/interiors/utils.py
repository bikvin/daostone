import os
from daosite import db
from flask import current_app
from werkzeug.utils import secure_filename
from daosite.models import InteriorImage


def save_interior_images(files, interior):
    directory = os.path.join(current_app.root_path, 'static', 'interiors')
    if not os.path.exists(directory):
        os.makedirs(directory)

    for f in files:
        filename = secure_filename(f.filename)
        if filename:
            save_path = os.path.join(directory, filename)
            path = os.path.join('interiors', filename)
            f.save(save_path)
            image = InteriorImage(
                path=path,
                interior=interior
            )
            db.session.add(image)
            db.session.commit()
