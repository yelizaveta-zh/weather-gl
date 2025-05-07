from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer

from services.weather_service import WeatherService


class WeatherWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = WeatherService()
        self._setup_ui()
        self._setup_timer()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.label_city = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.label_temp = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.label_desc = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.label_icon = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        for item in (
                self.label_city,
                self.label_icon,
                self.label_temp,
                self.label_desc
        ):
            layout.addWidget(item)

    def _setup_timer(self):
        timer = QTimer(self)
        timer.timeout.connect(self.update_weather)
        timer.start(10 * 60 * 1000)
        self.update_weather()

    def update_weather(self):
        data = self.service.get_current_weather()
        self.label_city.setText(data["city"])
        self.label_temp.setText(f"{data['temp']} °C")
        self.label_desc.setText(data["description"])
        self.label_icon.setText(data["icon"])
