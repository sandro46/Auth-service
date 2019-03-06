import unittest, sys, os, time
import requests

sys.path.append(os.getcwd())

from app import db
from models import User, Token
from config import Configurator as config
from passlib.hash import bcrypt

from helpers import issueToken, saveTestRefreshToken

class userTest(unittest.TestCase):
    def test_user_get_returns_list(self):
        payload = {'login': 'testuser', 'password': 'testpasswd'}
        auth1 = requests.post('http://localhost:5000/auth/', json=payload)
        self.assertEqual(auth1.status_code, 200)
        auth1 = auth1.json()
        self.assertTrue(auth1)
        self.assertFalse(auth1['err'])
        self.assertTrue(isinstance(auth1['refresh_token'], str))
        self.assertTrue(isinstance(auth1['token'], str))

        res = requests.get('http://localhost:5000/user/', headers={
                "Authorization":"Bearer "+auth1['token']
            })
        self.assertEqual(res.status_code, 200)
        res = res.json()
        print("[i] Response is ", res)
        self.assertTrue(res)

    def test_user_get_one_returns_obj(self):
        payload = {'login': 'testuser', 'password': 'testpasswd'}
        auth1 = requests.post('http://localhost:5000/auth/', json=payload)
        self.assertEqual(auth1.status_code, 200)
        auth1 = auth1.json()
        self.assertTrue(auth1)
        self.assertFalse(auth1['err'])
        self.assertTrue(isinstance(auth1['refresh_token'], str))
        self.assertTrue(isinstance(auth1['token'], str))

        res = requests.get('http://localhost:5000/user/1', headers={
                "Authorization":"Bearer "+auth1['token']
            })
        self.assertEqual(res.status_code, 200)
        res = res.json()
        print("[i] Response is ", res)
        self.assertTrue(res)

if __name__ == '__main__':
    unittest.main()
