import json
from project import db
from project.api.models import User


def add_user(username="test", email="test@test.com", password="test"):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def add_inactive_user(username="test", email="test@test.com", password="test"):
    user = add_user(username, email, password)
    user.active = False
    db.session.commit()
    return user


def add_admin(username="test", email="test@test.com", password="test"):
    user = add_user(username, email, password)
    user.admin = True
    db.session.commit()
    return user


register_credentials = {
    "username": "test",
    "email": "test@test.com",
    "password": "test"
}


def register(client, credentials=register_credentials):
    response = client.post(
        "/auth/register",
        data=json.dumps(credentials),
        content_type="application/json"
    )
    return response


login_credentias = {
    "email": "test@test.com",
    "password": "test"
}


def log_in(client, credentials=login_credentias):
    response = client.post(
        "/auth/login",
        data=json.dumps(credentials),
        content_type="application/json"
    )
    return response


def logout(client, token):
    response = client.get(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response


def status(client, token):
    response = client.get(
        "/auth/status",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response


users_credentials = {
    "username": "test2",
    "email": "test2@test.com",
    "password": "test"
}


def add_users(client, token, credentials=users_credentials):
    response = client.post(
        "/users",
        data=json.dumps(credentials),
        content_type="application/json",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response


def get_user(client, id):
    response = client.get(f"/users/{id}")
    return response
