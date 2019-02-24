from app import app

####################
#### blueprints ####
####################

from blueprintes.auth.blueprint import auth
from blueprintes.user.blueprint import user
from blueprintes.product.blueprint import product
from blueprintes.prod_cat.blueprint import prod_cat
from blueprintes.prod_component.blueprint import prod_component

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(product, url_prefix='/product')
app.register_blueprint(prod_cat, url_prefix='/prod_cat')
app.register_blueprint(prod_component, url_prefix='/prod_component')

if __name__ == '__main__':
    app.run()
