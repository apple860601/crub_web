import os
base_dir=os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'hard to guess'
    MAIL_SERVER = os.environ.get('MAIL_SERVER','smtp.googlemail.com')
    MAIL_POST = int(os.environ.get('MAIL_PORT','587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS','true').lower() in ['true','on','1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI='mysql+cymysql://root:apple80558@localhost/flaskdb?charset=utf8mb4'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
        'mysql+pymysql://root:apple80558@localhost/flaskdb?charset=utf8mb4'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
        'mysql+cymysql://root:apple80558@localhost/testdb?charset=utf8mb4'

class ProductionConfig(Config):
    # TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'mysql+cymysql://root:apple80558@localhost/flaskdb?charset=utf8mb4'

config={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}