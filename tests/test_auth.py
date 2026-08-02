def test_login_success(client):
    client.post("/api/v1/users/", json={
        "email": "test@test.com",
        "password": "1234",
        "job": "백엔드",
        "location": "서울",
        "career": "신입",
        "skills": ["Java"],
        "interests": [],
    })
    res = client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": "1234",
    })
    assert res.status_code == 200
    assert "access_token" in res.json()


def test_login_wrong_password(client):
    client.post("/api/v1/users/", json={
        "email": "test@test.com",
        "password": "1234",
        "job": "백엔드",
        "location": "서울",
        "career": "신입",
        "skills": ["Java"],
        "interests": [],
    })
    res = client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": "wrongpassword",
    })
    assert res.status_code == 401


def test_login_not_found(client):
    res = client.post("/api/v1/auth/login", json={
        "email": "nouser@test.com",
        "password": "1234",
    })
    assert res.status_code == 401