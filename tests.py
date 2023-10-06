from datetime import datetime
import unittest
from fastapi.testclient import TestClient
from main import app

class TestCoilAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    # def test_create_coil(self):
    #     payload = {
    #         "id": 11,
    #         "length": 10,
    #         "weight": 25
    #     }
    #     response = self.client.post("/api/coil", json=payload)
    #     assert response.status_code == 200
    #     assert isinstance(response.json(), int)
    
    def test_get_coils(self):
        params = {
            "start_id": 0,
            "end_id": 10
        }
        response = self.client.get("/api/coil", params=params)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_delete_coil(self):
        # Assuming id 1 exists in the database
        response = self.client.delete("/api/coil/1")
        assert response.status_code == 200

    def test_get_coil_stats(self):
        payload = {
            "start_date": "2023-01-01",
            "end_date": "2023-12-02"
        }
        response = self.client.get("/api/coil/stats", params=payload)
        print(response.content)  # Debugging statement
        print(type(response.json()))  
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

if __name__ == '__main__':
    unittest.main()