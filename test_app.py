from fastapi.testclient import TestClient
from api import app
import json

client = TestClient(app)

def test_classify_text_success():
    request_data = {
        "query": "What is the best way to learn Python?",
        "options": {"multilabel": False},
        "classes": [
            {"class_id": "C1", "class_name": "Programming", "class_description": "Learning programming languages."},
            {"class_id": "C2", "class_name": "Cooking", "class_description": "Cooking techniques."}
        ]
    }
    response = client.post("/classify", json=request_data)
    assert response.status_code == 200
    assert "result" in response.json()
    assert "error" not in response.json()
    

def test_classify_text_error():
    request_data = {
        "query": "What is the best way to learn Python?",
        "options": {"multilabel": False},
        # Classes field is intentionally omitted
    }
    
    response = client.post("/classify", json=request_data)
    assert response.status_code == 422 

