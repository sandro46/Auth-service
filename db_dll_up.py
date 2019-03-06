from app import db
from models import *

# db.drop_all()
db.create_all()

# user_role = User_role(name='superadmin', descript="Высший уровень доступа(может всё)")
# db.session.add(user_role)
# user_role = User_role(name='resource_admin', descript="Администратор ресурса, на котором он создан")
# db.session.add(user_role)
# user_role = User_role(name='resource_manager', descript="Редактирует товары, скидки, бонусы и тд")
# db.session.add(user_role)
# user_role = User_role(name='client', descript="Управляет своими заказами и бонусами")
# db.session.add(user_role)
# db.session.commit()
