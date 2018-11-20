from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from config import Configurator
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# import view



def to_json(alchObj, fields=None):
    ul = []
    print ("[i][to_json] ", dir(alchObj))

    for i in alchObj:
        row = {}
        for field in [x for x in dir(i) if not x.startswith('_') and x != 'metadata' and x != 'query' and x != 'query_class']:
            if fields:
                for f in fields:
                    if f == field: row[field] = i.__dict__.get(field)
            else: row[field] = i.__dict__.get(field)
        ul.append(row)
    return ul

def sql_to_dict(alchObj):
    ul = []
    print ("[i][sql_to_dict] ", isinstance(alchObj, tuple))
    print ("[i][sql_to_dict] ", isinstance(alchObj, list))
    print("[i][sql_to_dict] sql alchemy object type is ", type(alchObj))
    if isinstance(alchObj, list):
        for i in alchObj:
            d = {}
            d = dict(zip(i.keys(), i))
            ul.append(d)
    elif isinstance(alchObj, tuple):
        ul = dict(zip(alchObj.keys(), alchObj))
    return ul

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
