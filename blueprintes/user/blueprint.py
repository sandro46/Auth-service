from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import jwt, sys, os, uuid
from passlib.hash import bcrypt
from config import Configurator as config
from middlewares.require_login import require_login

sys.path.append(os.getcwd())

from models import User, Token
from app import db

user = Blueprint('user', __name__)

@user.route('/', methods=['GET'])
@require_login
def index(*args, **kwargs):
    if request.method == 'GET':
        return 'OK', 201
