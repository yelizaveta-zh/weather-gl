import requests


class WeatherService:
    BASE_URL = "https://wttr.in/{city}?format=j1&lang=uk"

    def get_current_weather(self, city: str = "Kyiv") -> dict:
        try:
            resp = requests.get(self.BASE_URL.format(city=city), timeout=5)
            data = resp.json()["current_condition"][0]
            temp = data["temp_C"]
            desc = data["weatherDesc"][0]["value"]

            icon = "☀️" if "сон" in desc.lower() else "🌧" if "дощ" in desc.lower() else "🌥"
            return {"city": city, "temp": temp, "description": desc, "icon": icon}
        except Exception:
            return {
                "city": city,
                "temp": "-",
                "description": "N/A",
                "icon": "❓"
            }
