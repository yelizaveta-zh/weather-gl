from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gl.piramida_widget import PyraWidget
from services.weather_service import WeatherService


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("PyQt6 OpenGL + Weather"))
        self._setup_ui()

    def _setup_ui(self):
        central = QWidget(self)
        layout = QHBoxLayout(central)

        self.gl_widget = PyraWidget(self)
        btn_reset = QPushButton(self.tr("Reset position"))
        btn_reset.clicked.connect(self.gl_widget.reset_view)
        vbox_gl = QVBoxLayout()
        vbox_gl.addWidget(self.gl_widget)
        vbox_gl.addWidget(btn_reset)

        weather_box = QGroupBox(self.tr("Weather"))
        vbox_weather = QVBoxLayout()
        self.label_city = QLabel()
        self.label_temp = QLabel()
        self.label_desc = QLabel()
        self.label_icon = QLabel()
        btn_update = QPushButton(self.tr("Reset weather"))
        btn_update.clicked.connect(self._update_weather)

        for w in (
            self.label_city,
            self.label_icon,
            self.label_temp,
            self.label_desc,
            btn_update,
        ):
            vbox_weather.addWidget(w)
        weather_box.setLayout(vbox_weather)

        layout.addLayout(vbox_gl)
        layout.addWidget(weather_box)
        self.setCentralWidget(central)

    def _setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_weather)
        self.timer.start(10 * 60 * 1000)
        self._update_weather()

    def _update_weather(self):
        data = WeatherService().get_current_weather()
        self.label_city.setText(data["city"])
        self.label_temp.setText(f"{data['temp']} °C")
        self.label_desc.setText(data["description"])
        self.label_icon.setText(data["icon"])
