from fastapi.testclient import TestClient

from app.main import backend


client = TestClient(backend)


def test_get_login():
    response = client.get("/token")
    # Assert get method on token is not allowed
    assert response.status_code == 405


def test_post_login_success():
    response = client.post("/token", data={
        "username": "admin",
        "password": "password"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_post_login_failure():
    response = client.post("/token", data={
        "username": "admin",
        "password": "wrong_password"
    })
    assert response.status_code == 401

def test_post_loan_without_auth():
    response = client.post("/loan")
    assert response.status_code == 401


def test_post_loan_success(login_headers):
    resp = client.post("/loan", json={
        "amount": 100,
        "tenure": 1
    }, headers=login_headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "loan created"


def test_e2e(login_headers, login_headers_user):
    # create a loan
    resp = client.post("/loan", json={
        "amount": 100,
        "tenure": 1
    }, headers=login_headers_user)
    assert resp.status_code == 200
    assert resp.json()["message"] == "loan created"

    # view loans created by user
    resp = client.get("/loans", headers=login_headers_user)
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    loan_id = resp.json()[0]["loan_id"]
    payment_schedule = resp.json()[0]["payments"][0]['schedule']

    # make payment for loan - failure
    resp = client.post(f"/loan/{loan_id}/payment", headers=login_headers_user, json={
        "amount": 10,
        "schedule": payment_schedule
    })
    assert resp.status_code == 400
    assert resp.json() == {"detail": "loan is not approved"}

    # approve the loan
    resp = client.patch(f"/loan/{loan_id}/approve", headers=login_headers)
    assert resp.status_code == 200
    assert resp.json() == {'message': 'loan approved'}

    # make payment for loan - incorrect loan
    resp = client.post(f"/loan/{loan_id}/payment", headers=login_headers_user, json={
        "amount": "10",
        "schedule": payment_schedule
    })
    assert resp.status_code == 400
    assert resp.json() == {'detail': 'amount not sufficient to make payment'}

    # make payment for loan - incorrect schedule
    resp = client.post(f"/loan/{loan_id}/payment", headers=login_headers_user, json={
        "amount": "100",
        "schedule": "2023-01-01"
    })
    assert resp.status_code == 400
    assert resp.json() == {'detail': 'loan payment not found, check input date'}

    # make payment for loan - insuffeicent amount
    resp = client.post(f"/loan/{loan_id}/payment", headers=login_headers_user, json={
        "amount": "10",
        "schedule": payment_schedule
    })
    assert resp.status_code == 400

    # make payment for loan - success
    resp = client.post(f"/loan/{loan_id}/payment", headers=login_headers_user, json={
        "amount": "100",
        "schedule": payment_schedule
    })
    assert resp.status_code == 200
    assert resp.json() == {'message': 'ok'}

    # view loans by user - all paid
    resp = client.get("/loans", headers=login_headers_user)
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    loan_status = resp.json()[0]['status']
    assert loan_status == "paid"
