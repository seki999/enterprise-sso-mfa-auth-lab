from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def login_token() -> str:
    response = client.post("/auth/login", json={"user_id": "employee01", "password": "Password123!"})
    assert response.status_code == 200
    token = response.json()["token"]
    mfa = client.post("/auth/mfa/verify", json={"token": token, "approve": True})
    assert mfa.json()["success"] is True
    return token


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_login_success():
    response = client.post("/auth/login", json={"user_id": "employee01", "password": "Password123!"})
    assert response.json()["success"] is True
    assert response.json()["next_step"] == "mfa"


def test_login_failure():
    response = client.post("/auth/login", json={"user_id": "employee01", "password": "wrong"})
    assert response.json()["success"] is False


def test_mfa_success():
    response = client.post("/auth/login", json={"user_id": "admin01", "password": "Password123!"})
    token = response.json()["token"]
    mfa = client.post("/auth/mfa/verify", json={"token": token, "code": "123456"})
    assert mfa.json()["success"] is True


def test_mfa_failure():
    response = client.post("/auth/login", json={"user_id": "employee02", "password": "Password123!"})
    token = response.json()["token"]
    mfa = client.post("/auth/mfa/verify", json={"token": token, "code": "000000"})
    assert mfa.json()["success"] is False


def test_users():
    assert len(client.get("/users").json()) >= 5


def test_applications():
    assert len(client.get("/applications").json()) >= 5


def test_policies():
    assert len(client.get("/policies").json()) >= 6


def test_auth_logs():
    assert len(client.get("/auth-logs").json()) >= 20


def test_vpn_success():
    response = client.post("/vpn/login", json={"user_id": "employee01", "password": "Password123!", "approve_mfa": True})
    assert response.json()["success"] is True


def test_vpn_failure():
    response = client.post("/vpn/login", json={"user_id": "employee01", "password": "wrong", "approve_mfa": True})
    assert response.json()["success"] is False


def test_dashboard_requires_authenticated_session():
    token = login_token()
    response = client.get("/dashboard/summary", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["user"]["user_id"] == "employee01"
