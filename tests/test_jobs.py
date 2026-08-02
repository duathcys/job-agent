def get_token(client):
    client.post("/api/v1/users/", json={
        "email": "test@test.com",
        "password": "1234",
        "job": "백엔드",
        "location": "서울",
        "career": "신입",
        "skills": ["Java", "Spring"],
        "interests": [],
    })
    res = client.post("/api/v1/auth/login", json={
        "email": "test@test.com",
        "password": "1234",
    })
    return res.json()["access_token"]


def test_create_job(client):
    res = client.post("/api/v1/jobs/", json={
        "company": "네이버",
        "title": "백엔드 개발자",
        "required_skills": ["Java", "Spring"],
        "location": "서울",
        "career": "신입",
        "source": "원티드",
    })
    assert res.status_code == 200
    assert res.json()["company"] == "네이버"


def test_get_jobs(client):
    client.post("/api/v1/jobs/", json={
        "company": "카카오",
        "title": "서버 개발자",
        "required_skills": ["Java"],
        "location": "서울",
        "career": "신입",
        "source": "원티드",
    })
    res = client.get("/api/v1/jobs/")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_get_job_not_found(client):
    res = client.get("/api/v1/jobs/999")
    assert res.status_code == 404