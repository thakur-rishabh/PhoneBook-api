# reference: https://fastapi.tiangolo.com/advanced/testing-database/
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# setting root location
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Base
from main import app, get_session

# test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# creating testing local session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# overide function
def override_get_db():
    try:
        session = TestingSessionLocal()
        yield session
    finally:
        session.close()

app.dependency_overrides[get_session] = override_get_db

client = TestClient(app)

# test user detail entry in db
def test_create_phoneBook():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "Rishabh",
            "phoneNumber": "+1 (682)-313-8425"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["detail"] == "user is created"

# test post invalid entry
def test_create_phoneBook_invalid():
    response = client.post(
        "/PhoneBook/add",
        json={
            "name": "test",
            "phoneNumber": "<script>alert(“XSS”)</script>"
        }
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == {"ERROR": "Invalid name or phone number"}

# test delete entry using name
def test_delete_by_name():
    client.post(
        "/PhoneBook/add",
        json={
            "name": "Rishabh",
            "phoneNumber": "+1 (682)-313-8425"
        }
    )
    response = client.put(
        "/PhoneBook/deleteByName",
        json={
            "name": "Rishabh"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["detail"] == "user is removed successfully"

# test entry not found
def test_name_not_found():
    response = client.put(
        "/PhoneBook/deleteByName",
        json={
            "name": "test"
        }
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == {"ERROR": "name is not present"}

# test invalid name input
def test_delete_by_name_invalid():
    response = client.put(
        "/PhoneBook/deleteByName",
        json={
            "name": "Ron O’Henry-Smith-Barnes"
        }
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == {"ERROR": "Invalid name"}

# test phoneNumber delete
def test_delete_by_number():
    client.post(
        "/PhoneBook/add",
        json={
            "name": "Thakur",
            "phoneNumber": "+1 (342)-721-6884"
        }
    )
    response = client.put(
        "/PhoneBook/deleteByNumber",
        json={
            "phoneNumber": "+1 (342)-721-6884"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["detail"] == "user is removed successfully"

# test invalid phone number input
def test_delete_by_phone_invalid():
    response = client.put(
        "/PhoneBook/deleteByNumber",
        json={
            "phoneNumber": "+01 (703) 123-1234"
        }
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == {"ERROR": "Invalid phone number"}

# test entry not found
def test_number_not_found():
    response = client.put(
        "/PhoneBook/deleteByNumber",
        json={
            "phoneNumber": "+1 (342)-721-6884"
        }
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "phone number not present"