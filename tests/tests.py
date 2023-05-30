import unittest

from bs4 import BeautifulSoup
from flask import current_app

from app.app import app, db, Users


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()  # создает контекст приложения Flask для каждого теста
        self.app_context.push()  # активирует контекст приложения Flask
        db.create_all()

    def tearDown(self):
        """ Вызывается после каждого теста, чтобы удалить таблицы базы данных и закрыть контекст приложения"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """ Существует ли приложение """
        self.assertFalse(current_app is None)

    def test_root(self):
        """ Подключается ли  """
        response = self.app.test_client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        """ Создается ли user """
        new_user = Users(email='test@example.com', password='password')
        db.session.add(new_user)
        db.session.commit()
        found_user = Users.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.password, 'password')

    def test_signup_post_response(self):
        """ Проверка POST запроса к /signup """
        response = self.app.test_client().post('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_post_response(self):
        """ Проверка POST запроса к / """
        response = self.app.test_client().post('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_get_response(self):
        """ Проверка GET запроса к /main """
        response = self.app.test_client().get('/main')
        self.assertEqual(response.status_code, 200)

    def login(self, email, password):
        return self.app.test_client().post('/', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def signup(self, email, password):
        return self.app.test_client().post('/signup', data=dict(
            email=email,
            password=password,
        ), follow_redirects=True)

    def test_email_wrong_format(self):
        """ Проверка работы email формы на / """
        res = self.login('random_mail', 'randompassword')
        soup = BeautifulSoup(res.data, 'html.parser')
        block = soup.find('span', class_="error")
        self.assertEqual(block.text, 'Email incorrect format')

    def test_signup_wrong_format(self):
        """ Проверка работы email формы на /signup """
        res = self.signup('mail@mailcom', 'password')
        soup = BeautifulSoup(res.data, 'html.parser')
        block = soup.find('span', class_="error")
        self.assertEqual(block.text, 'Email incorrect format')


if __name__ == '__main__':
    unittest.main()
