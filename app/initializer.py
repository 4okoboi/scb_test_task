import requests
import time

class Initializer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        time.sleep(5)

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