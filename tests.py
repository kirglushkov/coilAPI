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

    def test_create_coil(self):
        payload = {
            "length": 10,
            "weight": 25
        }
        response = self.client.post("/api/coil", json=payload)
        assert response.status_code == 200
        assert isinstance(response.json(), int)
    
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
        params = {
            "start_date": "2023-01-01",
            "end_date": "2024-02-02"
        }
        start_datetime = datetime.strptime(params["start_date"], "%Y-%m-%d")
        end_datetime = datetime.strptime(params["end_date"], "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        response = self.client.get("/api/coil/stats", params={"start_date": start_datetime, "end_date":end_datetime })
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

if __name__ == '__main__':
    unittest.main()