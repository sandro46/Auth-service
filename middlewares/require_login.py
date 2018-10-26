import logging, jwt
from functools import wraps
from flask import request, jsonify
from config import Configurator as config

if config.TEST: secret = 'TEST'
else: secret = config.SECRET_KEY

def require_login(api_method):
    @wraps(api_method)

    def check_user(*args, **kwargs):
        print('========check_user is a live===========')
        auth_header = request.headers.get('Authorization')
        print('[i] auth_header = ', auth_header)
        print('======================================')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                payload = {}
                payload['err'] = 'Error login'
                return jsonify(payload), 401

            print('[i] auth_token = ', auth_token)
            if not auth_token:
                payload = {}
                payload['err'] = 'Error login'
                return jsonify(payload), 401

            try:
                data = jwt.decode(auth_token, secret, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                payload = {}
                payload['err'] = 'Token Expired'
                print('[err] ', payload['err'] )
                return jsonify(payload), 401
            print('[i] Data = ', data)
            print('[+] Auth OK')
            kwargs["user_data"] = data
            return api_method(*args, **kwargs)
        else:
            payload = {}
            payload['err'] = 'Error login'
            return jsonify(payload), 401

    return check_user
