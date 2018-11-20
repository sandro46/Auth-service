from app import db
from datetime import datetime
#
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    phone = db.Column(db.String(140))
    password = db.Column(db.CHAR(255))
    role_id = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now())
    __table_args__ = {"schema":"app"}

    """docstring for User."""
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User id: {}, name: {}>'.format(self.id, self.name)

class User_role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    descript = db.Column(db.String(512))
    __table_args__ = {"schema":"app"}

    def __init__(self, *args, **kwargs):
        super(User_role, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User id: {}, name: {}>'.format(self.id, self.name)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    token = db.Column(db.CHAR(255))
    created = db.Column(db.DateTime, default=datetime.now())
    __table_args__ = {"schema":"app"}

    """docstring for User."""
    def __init__(self, *args, **kwargs):
        super(Token, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User id: {}>'.format(self.id)
