from PyQt6.QtWidgets import (
    QColorDialog,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gl.piramida_widget import PyraWidget
from ui.weather_widget import WeatherWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("PyQt6 OpenGL + Weather"))
        self._setup_ui()

    def _setup_ui(self):
        central = QWidget(self)
        layout = QHBoxLayout(central)

        pyramid_group = QGroupBox(self.tr("3D Pyramid"))
        vbox_gl = QVBoxLayout(pyramid_group)
        self.gl_widget = PyraWidget(self, base_size=1.0, height=1.2)
        btn_reset = QPushButton(self.tr("Reset position"))
        btn_reset.clicked.connect(self.gl_widget.reset_view)
        btn_color = QPushButton(self.tr("Choose the color"))
        btn_color.clicked.connect(self.choose_color)
        vbox_gl.addWidget(self.gl_widget)
        vbox_gl.addWidget(btn_reset)
        vbox_gl.addWidget(btn_color)

        weather_group = QGroupBox(self.tr("Weather"))
        weather_widget = WeatherWidget(self)
        vbox_weather = QVBoxLayout(weather_group)
        vbox_weather.addWidget(weather_widget)

        layout.addWidget(pyramid_group, stretch=1)
        layout.addWidget(weather_group, stretch=0)
        self.setCentralWidget(central)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.gl_widget.set_color(color)
