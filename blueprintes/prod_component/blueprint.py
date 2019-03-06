from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import jwt, sys, os, uuid, json
from passlib.hash import bcrypt
from config import Configurator as config
from middlewares.require_login import require_login
from flask_cors import CORS, cross_origin

sys.path.append(os.getcwd())

from models import Prod_component, Prod_component_rel
from app import db, to_json, sql_to_dict

prod_component = Blueprint('prod_component', __name__)

@prod_component.route('/', methods=['GET', 'POST', 'PUT'])
@cross_origin(origin='*')
@require_login
def index(*args, **kwargs):
    if request.method == 'GET':
        print('[i] Kwargs is ', kwargs)
        prod_component = db.session.query( \
            Prod_component.id.label('value'), Prod_component.name.label('text'), Prod_component.desc \
        ).order_by("value desc").all()
        prod_component = sql_to_dict(prod_component)
        print("[i] prod_component query returns is", prod_component)
        return jsonify(prod_component)
    if request.method == 'POST':
        formData = json.loads(request.data)
        print('[i][prod_component/:post] Request is ', formData)
        prod_component = Prod_component(name=formData['text'], desc=formData['desc'])
        db.session.add(prod_component)
        db.session.commit()
        print('[i][prod_component/:post] Added prod_component id is ', prod_component.id)
        return jsonify({'id': prod_component.id})
    if request.method == 'PUT':
        formData = json.loads(request.data)
        print('[i][Prod_component/:PUT] Request is ', formData)

        prod_component = Prod_component.query.filter(Prod_component.id == formData['value']).update({
            'name': formData['text'],
            'desc': formData['desc'],
        })
        print('[i][Prod_component/:PUT] User id is ', prod_component)
        db.session.commit()
        return 'OK'

@prod_component.route('/<id>', methods=['GET', 'DELETE'])
@cross_origin(origin='*')
@require_login
def delProdComponent(*args, **kwargs):
    if request.method == 'DELETE':
        print("[i][Prod_component/id:delete] Prod_component request returns is ", kwargs['id'])
        res = Prod_component.query.filter(Prod_component.id == kwargs['id']).delete()
        print("[i][Prod_component/id:delete] Deleting Prod_component query result is ", res)
        res = Prod_component_rel.query.filter(Prod_component_rel.component_id == kwargs['id']).delete()
        print("[i][Prod_component/id:delete] Deleting Prod_component_rel query result is ", res)
        db.session.commit()
        return 'OK'
