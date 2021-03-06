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

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(255)) #название
    code = db.Column(db.String(255)) #Артикул
    price = db.Column(db.REAL()) #Цена
    count = db.Column(db.Integer) #Количество
    image = db.Column(db.String(255)) #изображение
    measure = db.Column(db.String(255)) #Единица измерения
    ball = db.Column(db.Integer) #баллы
    nds = db.Column(db.Integer) #Ндс
    sale = db.Column(db.CHAR(1)) #дествуют ли скидки

    cat = db.Column(db.Integer) #Категория
    office = db.Column(db.Integer) #Филиал
    desc = db.Column(db.Text) #Описание
    sect = db.Column(db.Integer) #Цех
    created = db.Column(db.DateTime, default=datetime.now()) #создание
    modif = db.Column(db.DateTime, default=datetime.now()) #Дата последнего изменения
    __table_args__ = {"schema":"app"}

    """docstring for Product."""
    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)


class Prod_cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255)) #название
    desc = db.Column(db.Text) #Описание
    created = db.Column(db.DateTime, default=datetime.now()) #создание
    __table_args__ = {"schema":"app"}

    """docstring for Prod_cat."""
    def __init__(self, *args, **kwargs):
        super(Prod_cat, self).__init__(*args, **kwargs)

class Prod_component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255)) #название
    desc = db.Column(db.Text) #Описание
    created = db.Column(db.DateTime, default=datetime.now()) #создание
    __table_args__ = {"schema":"app"}

    """docstring for Prod_cat."""
    def __init__(self, *args, **kwargs):
        super(Prod_component, self).__init__(*args, **kwargs)

class Prod_component_rel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    component_id = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now()) #создание
    __table_args__ = {"schema":"app"}

    """docstring for Prod_cat."""
    def __init__(self, *args, **kwargs):
        super(Prod_component_rel, self).__init__(*args, **kwargs)

class Prod_section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    office_id = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now()) #создание
    __table_args__ = {"schema":"app"}

    """docstring for Prod_section."""
    def __init__(self, *args, **kwargs):
        super(Prod_section, self).__init__(*args, **kwargs)


class Office(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    desc = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now()) #создание
    __table_args__ = {"schema":"app"}

    """docstring for Office."""
    def __init__(self, *args, **kwargs):
        super(Office, self).__init__(*args, **kwargs)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    address = db.Column(db.String(255))
    discount = db.Column(db.Integer)
    desc = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now()) #создание
    __table_args__ = {"schema":"app"}

    """docstring for Client."""
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)
