import json
import unittest
from project.tests.base import BaseTestCase
from project.tests.utils import add_user, add_admin, add_inactive_user,\
    log_in, add_users, get_user


class TestUserService(BaseTestCase):
    """Tests for the Users Service"""

    def test_users(self):
        """Ensure the /ping route behaves correctly"""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["message"], "pong!")

    def test_add_user(self):
        """Ensure a new user can be added to the database"""
        add_admin()
        with self.client:
            resp_login = log_in(self.client)
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = add_users(self.client, token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["message"], "test2@test.com was added!")

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty"""
        add_admin()
        with self.client:
            resp_login = log_in(self.client)
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = add_users(self.client, token, {})
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_add_user_empty_username(self):
        """
        Ensure error is thrown if the JSON object does not have a username key
        """
        add_admin()
        with self.client:
            resp_login = log_in(self.client)
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = add_users(
                self.client,
                token,
                {"email": "test2@test.com", "password": "test"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_add_user_duplicate_username(self):
        """
        Ensure error is thrown if the username already exists
        """
        add_admin()
        with self.client:
            resp_login = log_in(self.client)
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = add_users(
                self.client,
                token,
                {
                    "username": "test",
                    "email": "test2@test.com",
                    "password": "test"
                }
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_add_user_empty_email(self):
        """
        Ensure error is thrown if the JSON object does not have a email key
        """
        add_admin()
        with self.client:
            resp_login = log_in(self.client)
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = add_users(
                self.client,
                token,
                {"username": "test2", "password": "test"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists"""
        add_admin()
        with self.client:
            resp_login = log_in(self.client)
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = add_users(
                self.client,
                token,
                {
                    "username": "test2",
                    "email": "test@test.com",
                    "password": "test"
                }
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"],
                "Sorry. That email already exists"
            )

    def test_add_user_empty_password(self):
        """
        Ensure error is thrown if the JSON object does not have a password key
        """
        add_admin()
        with self.client:
            resp_login = log_in(self.client)
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = add_users(
                self.client,
                token,
                {"username": "test2", "email": "test2@test.com"}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Invalid payload")

    def test_single_user(self):
        """Ensure get single user behaves correctly"""
        user = add_user()
        with self.client:
            response = get_user(self.client, user.id)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(data["data"]["username"], "test")
            self.assertEqual(data["data"]["email"], "test@test.com")

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided"""
        with self.client:
            response = get_user(self.client, "invalid")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "User does not exist")

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist"""
        with self.client:
            response = get_user(self.client, 999)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "User does not exist")

    def test_all_users(self):
        """Ensure get all users behaves correctly"""
        add_user()
        add_user("test2", "test2@test.com", "test")
        with self.client:
            response = self.client.get("/users")
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data["status"], "success")
            self.assertEqual(len(data["data"]["users"]), 2)
            self.assertEqual(data["data"]["users"][0]["username"], "test")
            self.assertEqual(
                data["data"]["users"][0]["email"],
                "test@test.com"
            )
            self.assertTrue(data["data"]["users"][0]["active"])
            self.assertFalse(data["data"]["users"][0]["admin"])
            self.assertEqual(data["data"]["users"][1]["username"], "test2")
            self.assertEqual(
                data["data"]["users"][1]["email"],
                "test2@test.com"
            )
            self.assertTrue(data["data"]["users"][1]["active"])
            self.assertFalse(data["data"]["users"][1]["admin"])

    def test_main_no_users(self):
        """
        Ensure the main route behaves correctly
        when no users have been added to the database
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"All Users", response.data)
        self.assertIn(b"<p>No users!</p>", response.data)

    def test_main_with_users(self):
        """
        Ensure the main route behaves correctly
        when users have been added to the database
        """
        add_user()
        add_user("test2", "test2@test.com", "test")
        with self.client:
            response = self.client.get("/")
            self.assertEquals(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(b"test", response.data)
            self.assertIn(b"test2", response.data)

    def test_main_add_user(self):
        """Ensure a new user can be added to the database via a POST request"""
        with self.client:
            response = self.client.post(
                "/",
                data={
                    "username": "test",
                    "email": "test@test.com",
                    "password": "test"
                },
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"All Users", response.data)
            self.assertNotIn(b"<p>No users!</p>", response.data)
            self.assertIn(b"test", response.data)

    def test_add_user_inactive(self):
        add_inactive_user()
        with self.client:
            resp_login = log_in(self.client)
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = add_users(self.client, token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(data["message"], "Provide a valid auth token")

    def test_add_user_not_admin(self):
        add_user()
        with self.client:
            resp_login = log_in(self.client)
            token = json.loads(resp_login.data.decode())["auth_token"]
            response = add_users(self.client, token)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data["status"], "fail")
            self.assertEqual(
                data["message"],
                "You do not have permission to do that"
            )


if __name__ == "__main__":
    unittest.main()
