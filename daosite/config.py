import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = 'SECRET_KEY'
    # SECRET_KEY = os.urandom(24)
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db') #"mysql://bikvin:@localhost/mosaicdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'stone.dao@gmail.com'
    MAIL_PASSWORD = ''
