import unittest, sys, os, time
import requests

sys.path.append(os.getcwd())

from app import db
from models import User, Token
from config import Configurator as config
from passlib.hash import bcrypt

from helpers import issueToken, saveTestRefreshToken




class authTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        h = bcrypt.hash("testpasswd")
        user1 = User.query.filter(User.id == 1).first()
        if not user1:
            user1 = User(id=1, name='testuser', phone='79508765464', password=h)
            db.session.add(user1)
        user2 = User.query.filter(User.id == 2).first()
        if not user2:
            user2 = User(id=2, name='testuser2', phone='79000000000', password=h)
            db.session.add(user2)
        db.session.commit()
        print("==========Starting all the tests.====================")

    # @classmethod
    # def tearDownClass(cls):
    #     users = User.query.filter(User.id.in_([1,2])).all()
    #     for user in users:
    #         db.session.delete(user)
    #     tokens = Token.query.filter(Token.user_id.in_([1,2])).all()
    #     for token in tokens:
    #         db.session.delete(token)
    #     db.session.commit()
    #     users_cnt = User.query.filter(User.id.in_([1,2])).count()
    #     tokens_cnt = Token.query.filter(Token.user_id.in_([1,2])).count()
    #     print("==========All tests end. Fixture clered====================")

    def test_fixture_is_ok(self):
        users = User.query.filter(User.id.in_([1,2])).all()
        self.assertEqual(users[0].name, 'testuser')
        self.assertEqual(users[1].name, 'testuser2')

    def test_decorator_on_root_path(self):
        res = requests.get('http://localhost:5000/')
        self.assertEqual(res.status_code, 200)

    def test_blueprint_get_returns_ok(self):
        res = requests.get('http://localhost:5000/auth/')
        self.assertEqual(res.text, 'OK')

    # User can successfully login
    def test_user_login(self):
        payload = {'login': 'testuser', 'passwd': 'testpasswd'}
        res = requests.post('http://localhost:5000/auth/', json=payload)
        res = res.json()
        self.assertTrue(res)
        self.assertFalse(res['err'])
        self.assertTrue(isinstance(res['refresh_token'], str))
        self.assertTrue(isinstance(res['token'], str))

        res = requests.post('http://localhost:5000/auth/refresh', json={'refresh_token': res['refresh_token']})
        self.assertEqual(res.status_code, 200)
        res = res.json()
        self.assertTrue(res)
        self.assertTrue(isinstance(res['refresh_token'], str))
        self.assertTrue(isinstance(res['token'], str))


    # User gets 403 on invalid creditionals successfully login
    def test_user_bad_creditionls_return_403(self):
        payload = {'login': 'testuser', 'passwd': 'bad_testpasswd'}
        res = requests.post('http://localhost:5000/auth/', json=payload)
        self.assertEqual(res.status_code, 403)

    #  User receives 401 on expired token
    def test_user_no_or_bad_token_return_401(self):
        res = requests.get('http://localhost:5000/user/', headers={
                "Authorization":"Bearer "+issueToken( {"id": "1", "exp": time.time()-1}, {  } ).decode('utf-8')
            })
        self.assertEqual(res.status_code, 401)

    # User receives 201 on not expired token
    def test_user_no_or_bad_token_return_201(self):
        res = requests.get('http://localhost:5000/user/', headers={
                "Authorization":"Bearer "+issueToken( {"id": "1", "exp": time.time()+10}, {  } ).decode('utf-8')
            })
        self.assertEqual(res.status_code, 201)

    # User can refresh access token using refresh token
    def test_user_get_access_token_using_refresh(self):
        payload = {}
        payload['refresh_token'] = 'REFRESH_TOKEN_TEST'
        saveTestRefreshToken(1, payload['refresh_token'])
        res = requests.post('http://localhost:5000/auth/refresh', json=payload)
        self.assertEqual(res.status_code, 200)
        res = res.json()
        self.assertTrue(res)
        self.assertFalse(res['err'])
        self.assertTrue(isinstance(res['refresh_token'], str))
        self.assertTrue(isinstance(res['token'], str))

    def test_user_get_404_on_invalid_refresh_token(self):
        res = requests.post('http://localhost:5000/auth/refresh', json={'refresh_token': 'INVALID_REFRESH_TOKEN_TEST'})
        self.assertEqual(res.status_code, 404)

    # TODO: User can use refresh token only once
    def test_user_can_use_refresh_token_only_once(self):
        payload = {}
        payload['refresh_token'] = 'REFRESH_TOKEN_TEST_ONCE'
        saveTestRefreshToken(1, payload['refresh_token'])
        res = requests.post('http://localhost:5000/auth/refresh', json=payload)
        res = requests.post('http://localhost:5000/auth/refresh', json=payload)
        self.assertEqual(res.status_code, 404)

    def test_refresh_tokens_become_invalid_on_logout(self):
        payload = {}
        payload['refresh_token'] = 'REFRESH_TOKEN_TEST_TO_DELETE_ON_LOGOUT'
        saveTestRefreshToken(2, payload['refresh_token'])
        res = requests.post('http://localhost:5000/auth/logout', headers={
                "Authorization":"Bearer "+issueToken( {"id": "2", "exp": time.time()+10}, {  } ).decode('utf-8')
            })
        self.assertEqual(res.status_code, 200)
        res = requests.post('http://localhost:5000/auth/refresh', json=payload)
        self.assertEqual(res.status_code, 404)

    def multiple_refresh_tokens_are_valid():
        payload = {'login': 'testuser', 'passwd': 'testpasswd'}
        auth1 = requests.post('http://localhost:5000/auth/', json=payload)
        auth1 = auth1.json()
        self.assertTrue(auth1)
        self.assertFalse(auth1['err'])
        self.assertTrue(isinstance(auth1['refresh_token'], str))
        self.assertTrue(isinstance(auth1['token'], str))

        auth2 = requests.post('http://localhost:5000/auth/', json=payload)
        auth2 = auth2.json()
        self.assertTrue(auth2)
        self.assertFalse(auth2['err'])
        self.assertTrue(isinstance(auth2['refresh_token'], str))
        self.assertTrue(isinstance(auth2['token'], str))

        payload['refresh_token'] = auth1['refresh_token']
        refresh1 = requests.post('http://localhost:5000/auth/refresh', json=payload)
        self.assertEqual(refresh1.status_code, 200)
        refresh1 = refresh1.json()
        self.assertTrue(refresh1)
        self.assertFalse(refresh1['err'])
        self.assertTrue(isinstance(refresh1['refresh_token'], str))
        self.assertTrue(isinstance(refresh1['token'], str))

        payload['refresh_token'] = auth1['refresh_token']
        refresh2 = requests.post('http://localhost:5000/auth/refresh', json=payload)
        self.assertEqual(refresh2.status_code, 200)
        refresh2 = refresh2.json()
        self.assertTrue(refresh2)
        self.assertFalse(refresh2['err'])
        self.assertTrue(isinstance(refresh2['refresh_token'], str))
        self.assertTrue(isinstance(refresh2['token'], str))




if __name__ == '__main__':
    unittest.main()
