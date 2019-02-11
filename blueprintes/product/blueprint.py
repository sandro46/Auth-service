from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import jwt, sys, os, uuid, json
from passlib.hash import bcrypt
from config import Configurator as config
from middlewares.require_login import require_login
from flask_cors import CORS, cross_origin

sys.path.append(os.getcwd())

from models import Product, Prod_cat
from app import db, to_json, sql_to_dict

product = Blueprint('product', __name__)


@product.route('/', methods=['GET', 'POST', 'PUT'])
@cross_origin(origin='*')
@require_login
def index(*args, **kwargs):
    if request.method == 'GET':
        print('[i] Kwargs is ', kwargs)
        product = db.session.query(Product.id, Product.name, Product.code, Product.price, Product.count, Product.image, Product.ball, Product.nds, Product.sale, Product.cat,  Product.office, Product.desc, Product.sect, Product.created, Product.modif, Product.measure, Prod_cat.name.label('category') ).outerjoin(Prod_cat, Prod_cat.id == Product.id).all()
        product = sql_to_dict(product)
        print("[i] Product query returns is", product)
        return jsonify(product)
    if request.method == 'POST':
        formData = json.loads(request.data)
        print('[i][product/:post] Request is ', formData)
        formData['ball'] = formData['ball'] if formData['ball'] else None

        product = Product(\
                            name=formData['name'], code=formData['code'], user_id=kwargs['user_data']['id'],\
                            price=formData['price'], count=formData['count'], measure=formData['measure'], \
                            ball=formData['ball'], nds=formData['nds'], cat=formData['cat'], sale=formData['sale'], desc=formData['desc'] \
                        )
        db.session.add(product)
        db.session.commit()
        print('[i][product/:post] Added product id is ', product.id)
        return jsonify({'id': product.id})
    if request.method == 'PUT':
        formData = json.loads(request.data)
        print('[i][Product/:PUT] Request is ', formData)

        product = Product.query.filter(Product.id == formData['id']).update({
            'ball': formData['ball']  if formData['ball'] else None,
            'cat': formData['cat']  if formData['cat'] else None,
            'code': formData['code']  if formData['code'] else None,
            'desc': formData['desc']  if formData['desc'] else None,
            'measure': formData['measure']  if formData['measure'] else None,
            'name': formData['name']  if formData['name'] else None,
            'nds': formData['nds']  if formData['nds'] else None,
            'office': formData['office']  if formData['office'] else None,
            'price': formData['price']  if formData['price'] else None,
            'sale': formData['sale']  if formData['sale'] else None,
            'sect': formData['sect']  if formData['sect'] else None
        })
        print('[i][product/:put] User id is ', product)
        db.session.commit()
        return 'OK'


@product.route('/<id>', methods=['GET', 'DELETE'])
@cross_origin(origin='*')
@require_login
def getProduct(*args, **kwargs):
    print("[i][getUser] kwargs is ", kwargs)
    if request.method == 'GET':
        users = db.session.query(User.id, User.name, User.phone, User_role.name.label('role_name'), User.role_id)\
            .join(User_role, User_role.id == User.role_id)\
            .filter(User.id == kwargs['id']).first()
        user = sql_to_dict(users)
        print("[i] User query returns is", user)
        return jsonify(user)
    if request.method == 'DELETE':
        print("[i][PRODUCT/id:delete] PRODUCT request returns is ", kwargs['id'])
        res = Product.query.filter(Product.id == kwargs['id']).delete()
        print("[i][PRODUCT/id:delete] Deleting query result is ", res)
        db.session.commit()
        return 'OK'

@product.route('/roles', methods=['GET'])
@cross_origin(origin='*')
@require_login
def getUserRoles(*args, **kwargs):
    if request.method == 'GET':
        roles = db.session.query(User_role.id.label('value'), User_role.name.label('text')).all()
        print("[i][getUserRoles]  Roles query returns is ", roles)
        roles = sql_to_dict(roles)
        print("[i][getUserRoles]  Roles modificate to ", roles)
        return jsonify(roles)
