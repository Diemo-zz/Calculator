from .main import app
from fastapi.testclient import TestClient
from base64 import b64encode

client = TestClient(app)


def get_api_from_query(query):
    query = b64encode(query.encode())
    query = query.decode("utf-8")
    api_call = "/calculus?query={query}".format(query=query)
    return api_call


def test_get_complicated_brackets():
    api_call = get_api_from_query("1 + (1(1+1(1-1+1) -1) +1*1/1 -1)")
    response = client.get(api_call)
    assert response.status_code == 200
    assert response.json() == {"result": 2.0, "error": False}


def test_bad_query():
    query = "bad query"
    api_call = get_api_from_query(query)
    response = client.get(api_call)
    assert response.status_code == 400
    assert response.json().get("error") is True


def test_with_floats():
    api_call = get_api_from_query("4.5+2.3")
    response = client.get(api_call)
    assert response.status_code == 200
    assert response.json() == {"result": 6.8, "error": False}


def test_with_bad_floats():
    api_call = get_api_from_query("4.5+6.4.5")
    response = client.get(api_call)
    assert response.status_code == 400
