from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import jwt, sys, os, uuid, json
from passlib.hash import bcrypt
from config import Configurator as config
from middlewares.require_login import require_login
from flask_cors import CORS, cross_origin

sys.path.append(os.getcwd())

from models import Prod_cat
from app import db, to_json, sql_to_dict

prod_cat = Blueprint('prod_cat', __name__)

@prod_cat.route('/', methods=['GET', 'POST', 'PUT'])
@cross_origin(origin='*')
@require_login
def index(*args, **kwargs):
    if request.method == 'GET':
        print('[i] Kwargs is ', kwargs)
        prod_cat = db.session.query( Prod_cat.id.label('value'), Prod_cat.name.label('text') ).all()
        prod_cat = sql_to_dict(prod_cat)
        print("[i] Prod_cat query returns is", prod_cat)
        return jsonify(prod_cat)
    if request.method == 'POST':
        formData = json.loads(request.data)
        print('[i][Prod_cat/:post] Request is ', formData)

        prodCat = Prod_cat(name=formData['text'])
        db.session.add(prodCat)
        db.session.commit()
        print('[i][Prod_cat/:post] Added Prod_cat id is ', prodCat.id)
        return jsonify({'id': prodCat.id})
    if request.method == 'PUT':
        formData = json.loads(request.data)
        print('[i][Prod_cat/:PUT] Request is ', formData)

        prodCat = Prod_cat.query.filter(Prod_cat.id == formData['value']).update({
            'name': formData['text']
        })
        print('[i][Prod_cat/:PUT] User id is ', prodCat)
        db.session.commit()
        return 'OK'

@prod_cat.route('/<id>', methods=['GET', 'DELETE'])
@cross_origin(origin='*')
@require_login
def getProdCat(*args, **kwargs):
    if request.method == 'DELETE':
        print("[i][ProdCat/id:delete] ProdCat request returns is ", kwargs['id'])
        res = Prod_cat.query.filter(Prod_cat.id == kwargs['id']).delete()
        print("[i][ProdCat/id:delete] Deleting query result is ", res)
        db.session.commit()
        return 'OK'
