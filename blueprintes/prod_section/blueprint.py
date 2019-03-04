from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import jwt, sys, os, uuid, json
from passlib.hash import bcrypt
from config import Configurator as config
from middlewares.require_login import require_login
from flask_cors import CORS, cross_origin

sys.path.append(os.getcwd())

from models import Prod_section as Model
from app import db, to_json, sql_to_dict

bpName = 'Prod_section'

bp = Blueprint(bpName, __name__)


@bp.route('/', methods=['GET', 'POST', 'PUT'])
@cross_origin(origin='*')
@require_login
def index(*args, **kwargs):
    if request.method == 'GET':
        print('[i] Kwargs is ', kwargs)
        res = db.session.query( \
            Model.id.label('value'), Model.name.label('text') \
        ).order_by("value desc").all()
        res = sql_to_dict(res)
        print("[i] {} query returns is ".format(bpName), res)
        return jsonify(res)
    if request.method == 'POST':
        formData = json.loads(request.data)
        print('[i][{}/:post] Request is '.format(bpName), formData)
        res = Model(name=formData['text'], office_id=formData['office_id'])
        db.session.add(res)
        db.session.commit()
        print('[i][{}/:post] Added Model id is '.format(bpName), res.id)
        return jsonify({'value': res.id})
    if request.method == 'PUT':
        formData = json.loads(request.data)
        print('[i][{}/:PUT] Request is '.format(bpName), formData)

        res = Model.query.filter(Model.id == formData['value']).update({
            'name': formData['text'],
            'address': formData['address'],
            'desc': formData['desc'],
        })
        print('[i][{}/:PUT] User id is '.format(bpName), res)
        db.session.commit()
        return 'OK'

@bp.route('/<id>', methods=['GET', 'DELETE'])
@cross_origin(origin='*')
@require_login
def delObject(*args, **kwargs):
    if request.method == 'DELETE':
        print("[i][{}/id:delete] request id ".format(bpName), kwargs['id'])
        res = Model.query.filter(Model.id == kwargs['id']).delete()
        print("[i][{}/id:delete] Deleting Model query result is ".format(bpName), res)
        db.session.commit()
        return 'OK'
