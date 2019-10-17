import unittest
import time
from sqlalchemy.exc import IntegrityError
from flask import current_app
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user("justatest", "test@test.com", "greaterthaneight")
        self.assertTrue(user.id)
        self.assertEqual(user.username, "justatest")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.password)
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        add_user("justatest", "test@test.com", "greaterthaneight")
        duplicate_user = User(
            username="justatest",
            email="test@test2.com",
            password="greaterthaneight"
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user("justatest", "test@test.com", "greaterthaneight")
        duplicate_user = User(
            username="justanothertest",
            email="test@test.com",
            password="greaterthaneight"
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user("justatest", "test@test.com", "greaterthaneight")
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user_one = add_user("justatest", "test@test.com", "greaterthaneight")
        user_two = add_user("justatest2", "test@test2.com", "greaterthaneight")
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        user = add_user("justatest", "test@test.com", "test")
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = add_user("justatest", "test@test.com", "test")
        auth_token = user.encode_auth_token(user.id)
        self.assertEqual(user.decode_auth_token(auth_token), user.id)

    def test_auth_token_incorrect_user_id(self):
        user = add_user("justatest", "test@test.com", "test")
        auth_token = user.encode_auth_token(user.id + 1)
        self.assertFalse(user.id == user.decode_auth_token(auth_token))

    def test_incorrect_auth_token(self):
        user = add_user("justatest", "test@test.com", "test")
        auth_token = b"testIncorrectAuthToken"
        self.assertEquals(
            "Invalid token. Please log in again.",
            user.decode_auth_token(auth_token)
        )

    def test_expired_auth_token(self):
        user = add_user("justatest", "test@test.com", "test")
        auth_token = user.encode_auth_token(user.id)
        time.sleep(current_app.config.get("TOKEN_EXPIRATION_SECONDS") + 1)
        self.assertEquals(
            "Signature expired. Please log in again.",
            user.decode_auth_token(auth_token)
        )

    def test_two_auth_tokens_for_one_user_match(self):
        user = add_user("justatest", "test@test.com", "test")
        first_auth_token = user.encode_auth_token(user.id)
        second_auth_token = user.encode_auth_token(user.id)
        self.assertEqual(first_auth_token, second_auth_token)


if __name__ == "__main__":
    unittest.main()
