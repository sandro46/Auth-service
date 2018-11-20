from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import jwt, sys, os, uuid, json
from passlib.hash import bcrypt
from config import Configurator as config
from middlewares.require_login import require_login
from flask_cors import CORS, cross_origin

sys.path.append(os.getcwd())

from models import User, User_role
from app import db, to_json, sql_to_dict

user = Blueprint('user', __name__)



@user.route('/', methods=['GET', 'POST', 'PUT'])
@cross_origin(origin='*')
@require_login
def index(*args, **kwargs):
    if request.method == 'GET':
        users = db.session.query(User.id, User.name, User.phone, User_role.name.label('role_name'), User.role_id)\
                    .join(User_role, User_role.id == User.role_id).all()
        users = sql_to_dict(users)
        print("[i] User query returns is", users)
        return jsonify(users)
    if request.method == 'POST':
        formData = json.loads(request.data)
        print('[i][user/:put] Request is ', formData)
        user = User(name=formData['name'], role_id=formData['role_id'], phone=formData['phone'])
        db.session.add(user)
        db.session.commit()
        print('[i][user/:put] Added user id is ', user.id)
        # user = to_json(user)
        return jsonify({'id': user.id})
    if request.method == 'PUT':
        formData = json.loads(request.data)
        print('[i][user/:post] Request is ', formData)
        user = User.query.filter(User.id == formData['id']).update({
            'name': formData['name'],
            'phone': formData['phone'],
            'role_id': formData['role_id']
        })
        print('[i][user/:post] User id is ', user)
        db.session.commit()
        return 'OK'


@user.route('/<user_id>', methods=['GET', 'DELETE'])
@cross_origin(origin='*')
@require_login
def getUser(*args, **kwargs):
    print("[i][getUser] kwargs is ", kwargs)
    if request.method == 'GET':
        users = db.session.query(User.id, User.name, User.phone, User_role.name.label('role_name'), User.role_id)\
            .join(User_role, User_role.id == User.role_id)\
            .filter(User.id == kwargs['user_id']).first()
        user = sql_to_dict(users)
        print("[i] User query returns is", user)
        return jsonify(user)
    if request.method == 'DELETE':
        print("[i][user/id:delete] User request returns is ", kwargs['user_id'])
        res = User.query.filter(User.id == kwargs['user_id']).delete()
        print("[i][user/id:delete] Deleting query result is ", res)
        db.session.commit()
        return 'OK'

@user.route('/roles', methods=['GET'])
@cross_origin(origin='*')
@require_login
def getUserRoles(*args, **kwargs):
    if request.method == 'GET':
        roles = db.session.query(User_role.id.label('value'), User_role.name.label('text')).all()
        print("[i][getUserRoles]  Roles query returns is ", roles)
        roles = sql_to_dict(roles)
        print("[i][getUserRoles]  Roles modificate to ", roles)
        return jsonify(roles)
