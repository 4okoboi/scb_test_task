import requests
import time

def make_requests():
    time.sleep(10)  # Задержка в 10 секунд

    payload_admin = {
            "username": "test_admin",
            "email": "admin@test.ru",
            "password": "test"
        }


    requests.post(
        url="http://localhost:8000/user/admin",
        json=payload_admin
    )

    payload_client = {
        "username":  'ООО "ООО"',
        "password": "client",
        "email": "client@test.ru",
        "actual_address": "Казань, Аметьево, 20"
    }

    requests.post(
        url="http://localhost:8000/user/client",
        json=payload_client
    )

if __name__ == "__main__":
    make_requests()