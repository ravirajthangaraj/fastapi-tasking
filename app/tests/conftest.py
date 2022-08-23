
from main import application
from fastapi.testclient import TestClient

client = TestClient(application)
