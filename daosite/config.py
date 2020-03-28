import os


class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = ''
    # SECRET_KEY = os.urandom(24)
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = "mysql://bikvin:@localhost/mosaicdb"

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'stone.dao@gmail.com'
    MAIL_PASSWORD = ''
