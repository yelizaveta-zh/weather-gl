import logging
import requests

from requests.exceptions import (
    HTTPError,
    Timeout,
    ConnectionError
)


BASE_URL = "https://wttr.in/{city}?format=j1&lang=uk"
ICON_MAP = {
    "sun": "☀️",
    "rain": "🌧",
    "clouds": "☁️",
    "snow": "❄️",
    "fog": "🌫",
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class WeatherService:
    def get_current_weather(self, city: str = "Kyiv") -> dict:
        try:
            raw = self._fetch_weather(city)
            return self._parse_weather_data(raw, city)
        except Timeout:
            logger.warning(f"Timeout when requesting weather for {city}")
            return self._default_response(city, "Timeout")
        except ConnectionError:
            logger.error(
                f"Connection error while retrieving weather for {city}"
            )
            return self._default_response(city, "No Connection")
        except HTTPError as http_err:
            status = http_err.response.status_code if http_err.response else "Unknown"
            logger.error(f"HTTP {status} when receiving weather for {city}")
            return self._default_response(city, f"HTTP {status}")
        except Exception as e:
            logger.exception(f"Unknown error while getting weather: {e}")
            return self._default_response(city, "Error")

    def _fetch_weather(self, city: str) -> dict:
        response = requests.get(BASE_URL.format(city=city), timeout=5)
        response.raise_for_status()
        return response.json()

    def _parse_weather_data(self, data: dict, city: str) -> dict:
        current = data.get("current_condition", [{}])[0]
        temp = current.get("temp_C", "-")
        desc = current.get("weatherDesc", [{}])[0].get("value", "N/A")
        icon = self._map_icon(desc.lower())
        return {"city": city, "temp": temp, "description": desc, "icon": icon}

    def _map_icon(self, description: str) -> str:
        for keyword, icon in ICON_MAP.items():
            if keyword in description:
                return icon
        return "🌥"

    def _default_response(self, city: str, err: str) -> dict:
        return {"city": city, "temp": "-", "description": err, "icon": "❓"}
