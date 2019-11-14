import json
import unittest
from flask import current_app
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user, test_user


class TestAuthBlueprint(BaseTestCase):
    def test_user_registration(self):
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps(test_user),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["message"], "Successfully registered")
            self.assertTrue(data["auth_token"])

    def test_user_registration_duplicate_email(self):
        add_user("test", "michael@mherman.org", "test")
        with self.client:
            response = self.client.post(
                "auth/register",
                data=json.dumps(test_user),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"],
                "Sorry. That user already exists"
            )

    def test_user_registration_duplicate_username(self):
        add_user("michael", "test@test.com", "test")
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps(test_user),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                "Sorry. That user already exists",
                data["message"]
            )

    def test_user_registration_empty_json(self):
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps({}),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_user_registration_no_username(self):
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps({
                    "email": "test@test.com",
                    "password": "test"
                }),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_user_registration_no_email(self):
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps({
                    "username": "justatest",
                    "password": "test"
                }),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_user_registration_no_password(self):
        with self.client:
            response = self.client.post(
                "/auth/register",
                data=json.dumps({
                    "username": "justatest",
                    "email": "test@test.com"
                }),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_registered_user_login(self):
        add_user("test", "test@test.com", "test")
        with self.client:
            response = self.client.post(
                "/auth/login",
                data=json.dumps({
                    "email": "test@test.com",
                    "password": "test"
                }),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["message"], "Successfully logged in")
            self.assertTrue(data["auth_token"])

    def test_user_login_no_json(self):
        add_user("test", "test@test.com", "test")
        with self.client:
            response = self.client.post(
                "/auth/login",
                data=json.dumps({}),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_user_login_no_email(self):
        add_user("test", "test@test.com", "test")
        with self.client:
            response = self.client.post(
                "/auth/login",
                data=json.dumps({"password": "test"}),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "User does not exist")

    def test_user_login_incorrect_email(self):
        add_user("test", "test@test.com", "test")
        with self.client:
            response = self.client.post(
                "/auth/login",
                data=json.dumps({
                    "email": "testing@test.com",
                    "password": "test"
                }),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "User does not exist")

    def test_user_login_no_password(self):
        add_user("test", "test@test.com", "test")
        with self.client:
            response = self.client.post(
                "/auth/login",
                data=json.dumps({"email": "test@test.com"}),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Incorrect password")

    def test_user_login_incorrent_password(self):
        add_user("test", "test@test.com", "test")
        with self.client:
            response = self.client.post(
                "/auth/login",
                data=json.dumps({
                    "email": "test@test.com",
                    "password": "testing"
                }),
                content_type="application/json"
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Incorrect password")

    def test_valid_logout(self):
        add_user("test", "test@test.com", "test")
        with self.client:
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({
                    "email": "test@test.com",
                    "password": "test"
                }),
                content_type="application/json"
            )
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.get(
                "/auth/logout",
                headers={"Authorization": f"Bearer {token}"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["message"], "Successfully logged out")

    def test_invalid_logout_expired_token(self):
        add_user("test", "test@test.com", "test")
        current_app.config["TOKEN_EXPIRATION_SECONDS"] = -1
        with self.client:
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({
                    "email": "test@test.com",
                    "password": "test"
                }),
                content_type="application/json"
            )
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.get(
                "/auth/logout",
                headers={"Authorization": f"Bearer {token}"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"],
                "Signature expired. Please log in again"
            )

    def test_invalid_logout(self):
        with self.client:
            response = self.client.get(
                "/auth/logout",
                headers={"Authorization": "Bearer invalid"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"],
                "Invalid token. Please log in again"
            )

    def test_user_status(self):
        add_user("test", "test@test.com", "test")
        with self.client:
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({
                    "email": "test@test.com",
                    "password": "test"
                }),
                content_type="application/json"
            )
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.get(
                "/auth/status",
                headers={"Authorization": f"Bearer {token}"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertTrue(data["data"] is not None)
            self.assertEqual(data["data"]["username"], "test")
            self.assertEqual(data["data"]["email"], "test@test.com")
            self.assertTrue(data["data"]["active"])

    def test_invalid_status(self):
        with self.client:
            response = self.client.get(
                "/auth/status",
                headers={"Authorization": "Bearer invalid"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"],
                "Invalid token. Please log in again"
            )

    def test_invalid_logout_inactive(self):
        add_user("test", "test@test.com", "test")
        user = User.query.filter_by(email="test@test.com").first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({
                    "email": "test@test.com",
                    "password": "test"
                }),
                content_type="application/json"
            )
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.get(
                "/auth/logout",
                headers={"Authorization": f"Bearer {token}"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Provide a valid auth token")

    def test_invalid_status_inactive(self):
        add_user("test", "test@test.com", "test")
        user = User.query.filter_by(email="test@test.com").first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                "/auth/login",
                data=json.dumps({
                    "email": "test@test.com",
                    "password": "test"
                }),
                content_type="application/json"
            )
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = self.client.get(
                "/auth/status",
                headers={"Authorization": f"Bearer {token}"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Provide a valid auth token")


if __name__ == "__main__":
    unittest.main()
