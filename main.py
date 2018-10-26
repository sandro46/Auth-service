from app import app

####################
#### blueprints ####
####################

from blueprintes.auth.blueprint import auth
from blueprintes.user.blueprint import user

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(user, url_prefix='/user')

if __name__ == '__main__':
    app.run()
