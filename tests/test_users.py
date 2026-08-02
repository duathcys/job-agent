def test_create_user(client):
    res = client.post("/api/v1/users/", json={
        "email": "test@test.com",
        "password": "1234",
        "job": "백엔드",
        "location": "서울",
        "career": "신입",
        "skills": ["Java", "Spring", "MySQL"],
        "interests": ["네이버", "카카오"],
    })
    assert res.status_code == 200
    assert res.json()["email"] == "test@test.com"
    assert res.json()["job"] == "백엔드"


def test_create_duplicate_user(client):
    data = {
        "email": "test@test.com",
        "password": "1234",
        "job": "백엔드",
        "location": "서울",
        "career": "신입",
        "skills": ["Java", "Spring"],
        "interests": [],
    }
    client.post("/api/v1/users/", json=data)
    res = client.post("/api/v1/users/", json=data)
    assert res.status_code == 400


def test_get_user(client):
    client.post("/api/v1/users/", json={
        "email": "test@test.com",
        "password": "1234",
        "job": "백엔드",
        "location": "서울",
        "career": "신입",
        "skills": ["Java"],
        "interests": [],
    })
    res = client.get("/api/v1/users/1")
    assert res.status_code == 200
    assert res.json()["id"] == 1


def test_get_user_not_found(client):
    res = client.get("/api/v1/users/999")
    assert res.status_code == 404