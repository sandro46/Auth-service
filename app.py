from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from config import Configurator
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# import view


################
#### config ####
################

app = Flask(__name__)
app.config.from_object(Configurator)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



################
#### view ####
################



@app.route('/')
def index():
    return render_template('index.html')
#
# if __name__ == '__main__':
#     app.run()
