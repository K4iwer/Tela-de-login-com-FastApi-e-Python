# test_api.py
import requests

BASE_URL = "http://127.0.0.1:8000"  # ajuste se rodar no docker (ex: http://localhost:8000)

def test_register():
    payload = {
        "username": "Alberto",
        "email": "Alberto@example.com",
        "password": "999"
    }
    r = requests.post(f"{BASE_URL}/register", json=payload)
    print("REGISTER:", r.status_code, r.json())

def test_login():
    payload = {
        "username": "Alberto",
        "password": "999"
    }
    r = requests.post(f"{BASE_URL}/login", json=payload)
    print("LOGIN:", r.status_code, r.json())
    return r

def test_get_user(user_id):
    r = requests.get(f"{BASE_URL}/user/{user_id}")
    print("GET USER:", r.status_code, r.json())

def test_delete_user(user_id):
    r = requests.delete(f"{BASE_URL}/user/{user_id}")
    print("DELETE USER:", r.status_code, r.json())

def test_delete_user_byname(username):
    r = requests.delete(f"{BASE_URL}/user/byname/{username}")
    print("DELETE USER BYNAME:", r.status_code, r.json())

def test_logout():
    # Sessão para que os cookies sejam gerenciados automaticamente
    with requests.Session() as s:
        login_payload = {"username": "Alberto", "password": "999"}
        r_login = s.post(f"{BASE_URL}/login", json=login_payload)

        if r_login.status_code != 200:
            print("Falha no login, não é possível testar o logout.")
            print("Resposta do login:", r_login.text) 
            return
        
        csrf_token = s.cookies.get("csrf_access_token")

        headers = {
            "X-CSRF-TOKEN": csrf_token
        }

        r_logout = s.post(f"{BASE_URL}/logout", headers=headers)
        
        print("LOGOUT Status:", r_logout.status_code)
        print("LOGOUT Response:", r_logout.json())

def test_refresh():
    login_response = test_login()
    
    csrf_token = login_response.cookies.get("csrf_refresh_token")
    print("CSRF Refresh Token:", csrf_token)

    cookies = login_response.cookies
    
    headers = {
        "X-CSRF-TOKEN": csrf_token
    }
    
    r = requests.post(f"{BASE_URL}/refresh", headers=headers, cookies=cookies)
    print("Headers sent for refresh:", headers)
    print("REFRESH:", r.status_code)
    

def test_status():
    r = requests.get(f"{BASE_URL}/status")
    print("STATUS:", r.status_code, r.json())



test_register()
# token = test_login()
# test_get_user(9)
# test_delete_user(9)
# test_delete_user_byname("João")
# test_logout()
# test_refresh()
# test_status()
