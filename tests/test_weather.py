import pytest

import requests
from requests.exceptions import HTTPError, ConnectionError

from services.weather_service import WeatherService, ICON_MAP


class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            http_err = HTTPError(f"{self.status_code} Error")
            http_err.response = self
            raise http_err


@pytest.fixture
def service():
    return WeatherService()


def test_parse_weather_data_success(monkeypatch, service):
    sample = {
        "current_condition": [{
            "temp_C": "15",
            "weatherDesc": [{"value": "Rain"}]
        }]
    }
    resp = DummyResponse(sample, 200)
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: resp)

    result = service.get_current_weather("Kyiv")
    assert result["city"] == "Kyiv"
    assert result["temp"] == "15"
    assert "rain" in result["description"].lower()
    assert result["icon"] == ICON_MAP["rain"]


def test_http_error(monkeypatch, service):
    resp = DummyResponse({}, status_code=500)
    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: resp)

    result = service.get_current_weather("Kyiv")
    assert result["description"].startswith("HTTP")
    assert result["icon"] == "❓"


def test_connection_error(monkeypatch, service):
    monkeypatch.setattr(
        requests,
        "get",
        lambda *args, **kwargs: (_ for _ in ()).throw(ConnectionError())
    )
    result = service.get_current_weather("Kyiv")
    assert result["description"] == "No Connection"
    assert result["icon"] == "❓"
