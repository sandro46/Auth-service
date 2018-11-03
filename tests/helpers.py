import jwt, sys, os, uuid
sys.path.append(os.getcwd())
from config import Configurator as config
from models import Token
from app import db

def issueToken(data, options):
    return jwt.encode(data, 'TEST', algorithm='HS256', headers=options)

def saveTestRefreshToken(user_id, token):
    token = Token(user_id=user_id, token=token)
    db.session.add(token)
    db.session.commit()
    return True
