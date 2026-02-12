from fastapi.testclient import TestClient

def test_client(client: TestClient):
    assert type(client) == TestClient
