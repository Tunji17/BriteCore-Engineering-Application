import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', '5791628bb0b13ce0c676dfde280ba245')
    # app.config['SQLALCHEMY_DATABASE_URI'] =
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    # os.environ.get('DATABASE_URL') or \
     #    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
