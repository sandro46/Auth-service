from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import jwt, sys, os, uuid, json
from passlib.hash import bcrypt
from config import Configurator as config
from middlewares.require_login import require_login
from flask_cors import CORS, cross_origin

sys.path.append(os.getcwd())

from models import Product, Prod_cat, Prod_component_rel
from app import db, to_json, sql_to_dict

product = Blueprint('product', __name__)


@product.route('/', methods=['GET', 'POST', 'PUT'])
@cross_origin(origin='*')
@require_login
def index(*args, **kwargs):
    if request.method == 'GET':
        print('[i] Kwargs is ', kwargs)
        product = db.session.execute('''
            	SELECT
            		p.*,
            		cat.name category,
            		to_char(p.created, 'dd.mm.yyyy') created,
            		to_char(p.modif, 'dd.mm.yyyy') modif,
            		prod_comp.list components_list
            	FROM app.product p
            	left join app.prod_cat cat ON cat.id=p.cat
            	left join (
            		SELECT
            			 cr.product_id,
            			array_agg(cr.component_id) list
            		from app.prod_component_rel cr
            		group by cr.product_id
            	) prod_comp ON prod_comp.product_id=p.id
        ''')
        product = json.dumps([dict(row) for row in product])
        print("[i] Product query returns is", product)
        return jsonify(json.loads(product))
    if request.method == 'POST':
        formData = json.loads(request.data)
        print('[i][product/:post] Request is ', formData)
        formData['ball'] = formData['ball'] if formData['ball'] else None
        formData['nds'] = formData['nds'] if formData['nds'] else None
        formData['office'] = formData['office'] if formData['office'] else None

        product = Product(\
                            name=formData['name'], code=formData['code'], user_id=kwargs['user_data']['id'],\
                            price=formData['price'], count=formData['count'], measure=formData['measure'], \
                            ball=formData['ball'], nds=formData['nds'], cat=formData['cat'], \
                            sale=formData['sale'], desc=formData['desc'] \
                        )
        db.session.add(product)
        db.session.commit()
        print('[i][product/:post] Added product id is ', product.id)
        return jsonify({'id': product.id})
    if request.method == 'PUT':
        formData = json.loads(request.data)
        print('[i][Product/:PUT] Request is ', formData)

        # if(formData['components_list']):

        if(formData['components_list']):
            print('[i][Product/:PUT] Product_list is ', formData['components_list'])
            print('[i][Product/:PUT] Insert Product_list begin ')
            res = Prod_component_rel.query.filter(Prod_component_rel.product_id == formData['id']).delete()
            for e in formData['components_list']:
                component_rel = Prod_component_rel(product_id=formData['id'], component_id=e)
                db.session.add(component_rel)
            print('[i][Product/:PUT] Insert Product_list end ')

        product = Product.query.filter(Product.id == formData['id']).update({
            'ball': formData['ball']  if formData['ball'] else None,
            'cat': formData['cat']  if formData['cat'] else None,
            'code': formData['code']  if formData['code'] else None,
            'desc': formData['desc']  if formData['desc'] else None,
            'count': formData['count']  if formData['count'] else None,
            'measure': formData['measure']  if formData['measure'] else None,
            'name': formData['name']  if formData['name'] else None,
            'nds': formData['nds']  if formData['nds'] else None,
            'office': formData['office'] if formData['office'] and formData['office'] != 'null' else None,
            'price': formData['price']  if formData['price'] else None,
            'sale': formData['sale']  if formData['sale'] else None,
            'sect': formData['sect']  if formData['sect'] and formData['sect'] != 'null' else None
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
