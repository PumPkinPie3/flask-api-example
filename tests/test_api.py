import json
import unittest
import inspect
from app import create_app, db
from app.models import User


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = create_app().test_client()

        User.generate_dummy(id=1, name='user1', password='password', email='user1@example.com')

    def tearDown(self):
        User.query.delete()
        db.session.commit()
        db.session.remove()

    @classmethod
    def get_request_data(cls, name):
        file = './tests/request_data/{}.json'.format(name)
        with open(file) as json_file:
            data = json_file.read()
        return data

    def test_get_user(self):
        response = self.client.get('/users/1')
        body = json.loads(response.data.decode('utf-8'))

        self.assertTrue(response.status_code == 200)

        user = User.query.filter_by(id=1).one()
        self.assertTrue(body['id'] == user.id)

    def test_get_null_user(self):
        response = self.client.get('/users/2')
        body = json.loads(response.data.decode('utf-8'))

        self.assertTrue(response.status_code == 400)

        self.assertTrue(body['title'] == '[UserNotFound]')

    def test_add_user(self):
        name = inspect.currentframe().f_code.co_name
        data = self.get_request_data(name)
        response = self.client.post('/users', data=data, content_type='application/json')
        body = json.loads(response.data.decode('utf-8'))

        self.assertTrue(response.status_code == 200)

        user = User.query.filter_by(email='root@example.com').one()
        self.assertTrue(body['id'] == user.id)

    def test_delete_user(self):
        response = self.client.delete('/users/1')

        self.assertTrue(response.status_code == 200)

        users = User.query.filter_by(id=1).all()
        self.assertTrue(len(users) == 0)


if __name__ == '__main__':
    unittest.main()
