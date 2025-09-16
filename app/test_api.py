# test_api.py
import requests

BASE_URL = "http://127.0.0.1:8000"  # ajuste se rodar no docker (ex: http://localhost:8000)

def test_register():
    payload = {
        "id": 2,
        "username": "João",
        "email": "Joao@example.com",
        "password": "1234"
    }
    r = requests.post(f"{BASE_URL}/register", json=payload)
    print("REGISTER:", r.status_code, r.json())

def test_login():
    payload = {
        "username": "João",
        "password": "1234"
    }
    r = requests.post(f"{BASE_URL}/login", json=payload)
    print("LOGIN:", r.status_code, r.json())
    return r.json().get("access_token")

def test_get_user(user_id):
    r = requests.get(f"{BASE_URL}/user/{user_id}")
    print("GET USER:", r.status_code, r.json())

def test_delete_user(user_id):
    r = requests.delete(f"{BASE_URL}/user/{user_id}")
    print("DELETE USER:", r.status_code, r.json())

def test_delete_user_byname(username):
    r = requests.delete(f"{BASE_URL}/user/byname/{username}")
    print("DELETE USER BYNAME:", r.status_code, r.json())

def test_logout(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(f"{BASE_URL}/logout", headers=headers)
    print("LOGOUT:", r.status_code, r.json())

def test_refresh(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(f"{BASE_URL}/refresh", headers=headers)
    print("REFRESH:", r.status_code, r.json())

def test_status():
    r = requests.get(f"{BASE_URL}/status")
    print("STATUS:", r.status_code, r.json())



test_register()
token = test_login()
test_get_user(2)
test_delete_user(2)
test_delete_user_byname("João")
if token:
    test_refresh(token)
    test_logout(token)
test_status()
