import enum
from datetime import datetime
from main_app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class ProductEnum(enum.Enum):
    policies = 'Policies'
    billing = 'Billing'
    claims = 'Claims'
    report = 'Reports'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


     # def __repr__(self):
     #    return '<User %r>' % (self.username)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    request = db.relationship('Request', backref='client', lazy='dynamic')

    # def __repr__(self):
    #     return '<Client %r>' % (self.name)

    def __repr__(self):
       return f"<Client(name='{self.name}')>"


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    priority = db.Column(db.Integer)
    target_date = db.Column(db.Date)
    product = db.Column(db.Enum(ProductEnum))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # def __repr__(self):
    #     return '<Request %r>' % (self.client)

    def __repr__(self):
       return f"<Request(client='{self.client}', title='{self.title}', priority='{self.priority}')>"
