from main import app, data
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_countries():
    response = client.get("/countries")
    assert response.status_code == 200
    assert sorted(response.json()) == ["England", "France", "Germany", "Italy", "Peru", "Portugal", "Spain"]

def test_cities_spain():
    response = client.get("/countries/Spain/cities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_monthly_average_spain_city_month():
    # Use the first city and month from Spain for the test
    countries_resp = client.get("/countries")
    assert countries_resp.status_code == 200
    assert "Spain" in countries_resp.json()
    cities_resp = client.get("/countries/Spain/cities")
    assert cities_resp.status_code == 200
    cities = cities_resp.json()
    assert len(cities) > 0
    city = cities[0]
    # Get months for the city
    months = list(data["Spain"][city].keys())
    assert len(months) > 0
    month = months[0]
    avg_resp = client.get(f"/countries/Spain/{city}/{month}")
    assert avg_resp.status_code == 200
    assert avg_resp.json() == data["Spain"][city][month]