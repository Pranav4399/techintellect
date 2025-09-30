from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

def test_list_employees():
    response = client.get("/employees")
    assert response.status_code == 200
    assert "employees" in response.json()

def test_create_employee():
    data = {"Emp_ID": 1001, "Emp_Name": "John Doe"}
    response = client.post("/upload-data", json=data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_create_missing_id():
    data = {"Emp_Name": "Jane Doe"}
    response = client.post("/upload-data", json=data)
    assert response.status_code == 400

def test_update_employee():
    client.post("/upload-data", json={"Emp_ID": 2001, "Emp_Name": "Test"})
    response = client.put("/update-employee", json={"Emp_ID": 2001, "Designation": "Manager"})
    assert response.status_code == 200

def test_delete_employee():
    client.post("/upload-data", json={"Emp_ID": 3001, "Emp_Name": "Delete Me"})
    response = client.request("DELETE", "/delete-employee", json={"Emp_ID": 3001})
    assert response.status_code == 200
