from app import manager, db
from main import *
from models import User, Token


if __name__ == '__main__':
    manager.run()
    db.create_all()
