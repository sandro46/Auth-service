from app import db
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import jwt, sys, os, uuid
from passlib.hash import bcrypt
from config import Configurator as config
from middlewares.require_login import require_login

sys.path.append(os.getcwd())

from models import User, Token

auth = Blueprint('auth', __name__)

def releaseTokens(user_id):
    ret = {}
    ret['refresh_token'] = uuid.uuid4().hex
    ret['token'] = jwt.encode({ 'id': user_id }, config.secret, algorithm='HS256')
    ret['token'] = ret['token'].decode('utf-8')
    print('[+] New token is ', ret['refresh_token'])
    new_token = Token(user_id=user_id, token=ret['refresh_token'])
    db.session.add(new_token)
    db.session.commit()
    return ret

@auth.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return 'OK'
    if request.method == 'POST':
        payload = {}
        payload['err'] = ''
        req = request.json

        user = User.query.filter(User.name == req['login']).first()
        user.password = user.password.rstrip()

        if not bcrypt.verify(req['passwd'], user.password) or not user:
            payload['err'] = 'Bad Creditionals'
            print(payload['err'])
            return jsonify(payload), 403

        tokens = releaseTokens(user.id)
        payload['refresh_token'] = tokens['refresh_token']
        payload['token'] = tokens['token']
        return jsonify(payload), 200

@auth.route('/refresh', methods=['POST'])
def refresh_token():
    if request.method == 'POST':
        payload = {}
        payload['err'] = ''
        req = request.json

        print('[i] Refresh token in request is', req['refresh_token'])
        token = Token.query.filter(Token.token == req['refresh_token']).first()
        if not token:
            payload['err'] = 'Not valid or not Refresh Token'
            print('[err] ', payload['err'] )
            return jsonify(payload), 404

        tokens = releaseTokens(token.user_id)
        db.session.delete(token)
        db.session.commit()
        payload['refresh_token'] = tokens['refresh_token']
        payload['token'] = tokens['token']
        return jsonify(payload), 200

@auth.route('/logout', methods=['POST'])
@require_login
def logout(*args, **kwargs):
    print('[i] user data is ', kwargs['user_data'])
    print('[i] user data[id] is ', kwargs['user_data']['id'])
    Token.query.filter(Token.user_id==kwargs['user_data']['id']).delete()
    db.session.commit()
    return 'OK', 200
