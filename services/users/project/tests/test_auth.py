import json
import unittest
from flask import current_app
from project.tests.base import BaseTestCase
from project.tests.utils import add_user, add_inactive_user, log_in, register,\
    logout, status


class TestAuthBlueprint(BaseTestCase):
    def test_user_registration(self):
        with self.client:
            response = register(self.client)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["message"], "Successfully registered")
            self.assertTrue(data["auth_token"])

    def test_user_registration_duplicate_email(self):
        add_user()
        with self.client:
            response = register(self.client)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"],
                "Sorry. That user already exists"
            )

    def test_user_registration_duplicate_username(self):
        add_user()
        with self.client:
            response = register(self.client)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                "Sorry. That user already exists",
                data["message"]
            )

    def test_user_registration_empty_json(self):
        with self.client:
            response = register(self.client, {})
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_user_registration_no_username(self):
        with self.client:
            response = register(
                self.client,
                {"email": "test@test.com", "password": "test"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_user_registration_no_email(self):
        with self.client:
            response = register(
                self.client,
                {"username": "test", "password": "test"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_user_registration_no_password(self):
        with self.client:
            response = register(
                self.client,
                {"username": "test", "email": "test@test.com"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_registered_user_login(self):
        add_user()
        with self.client:
            response = log_in(self.client)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["message"], "Successfully logged in")
            self.assertTrue(data["auth_token"])

    def test_user_login_no_json(self):
        add_user()
        with self.client:
            response = log_in(self.client, {})
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_user_login_no_email(self):
        add_user()
        with self.client:
            response = log_in(self.client, {"password": "test"})
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "User does not exist")

    def test_user_login_incorrect_email(self):
        add_user()
        with self.client:
            response = log_in(
                self.client,
                {"email": "test2@test.com", "password": "test"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "User does not exist")

    def test_user_login_no_password(self):
        add_user()
        with self.client:
            response = log_in(self.client, {"email": "test@test.com"})
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Incorrect password")

    def test_user_login_incorrent_password(self):
        add_user()
        with self.client:
            response = log_in(
                self.client,
                {"email": "test@test.com", "password": "test2"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Incorrect password")

    def test_valid_logout(self):
        add_user()
        with self.client:
            resp_login = log_in(self.client)
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = logout(self.client, token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["message"], "Successfully logged out")

    def test_invalid_logout_expired_token(self):
        add_user()
        current_app.config["TOKEN_EXPIRATION_SECONDS"] = -1
        with self.client:
            resp_login = log_in(self.client)
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = logout(self.client, token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"],
                "Signature expired. Please log in again"
            )

    def test_invalid_logout(self):
        with self.client:
            response = logout(self.client, "invalid")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"],
                "Invalid token. Please log in again"
            )

    def test_user_status(self):
        add_user()
        with self.client:
            resp_login = log_in(self.client)
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = status(self.client, token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertTrue(data["data"] is not None)
            self.assertEqual(data["data"]["username"], "test")
            self.assertEqual(data["data"]["email"], "test@test.com")
            self.assertTrue(data["data"]["active"])
            self.assertFalse(data["data"]["admin"])

    def test_invalid_status(self):
        with self.client:
            response = status(self.client, "invalid")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"],
                "Invalid token. Please log in again"
            )

    def test_invalid_logout_inactive(self):
        add_inactive_user()
        with self.client:
            resp_login = log_in(self.client)
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = logout(self.client, token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Provide a valid auth token")

    def test_invalid_status_inactive(self):
        add_inactive_user()
        with self.client:
            resp_login = log_in(self.client)
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = status(self.client, token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Provide a valid auth token")


if __name__ == "__main__":
    unittest.main()
