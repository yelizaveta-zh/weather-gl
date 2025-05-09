from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QColorDialog,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
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
        pyramid_group.setFont(QFont("Arial", 12))
        vbox_gl = QVBoxLayout(pyramid_group)
        self.gl_widget = PyraWidget(self, base_size=0.7, height=1.5)

        btn_reset = QPushButton(self.tr("Reset position"))
        btn_reset.setFont(QFont("Arial", 10))
        btn_reset.clicked.connect(self.gl_widget.reset_view)

        btn_color = QPushButton(self.tr("Choose the color"))
        btn_color.setFont(QFont("Arial", 10))
        btn_color.clicked.connect(self.choose_color)

        btn_load = QPushButton(self.tr("Load the model"))
        btn_load.setFont(QFont("Arial", 10))
        btn_load.clicked.connect(self.load_model)

        vbox_gl.addWidget(self.gl_widget)
        vbox_gl.addWidget(btn_reset)
        vbox_gl.addWidget(btn_color)
        vbox_gl.addWidget(btn_load)

        weather_group = QGroupBox(self.tr("Weather"))
        weather_group.setFont(QFont("Arial", 12))
        weather_widget = WeatherWidget(self)
        vbox_weather = QVBoxLayout(weather_group)
        vbox_weather.addWidget(weather_widget)

        layout.addWidget(pyramid_group, stretch=2)
        layout.addWidget(weather_group, stretch=1)
        self.setCentralWidget(central)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.gl_widget.set_color(color)

    def load_model(self):
        filename, _ = QFileDialog.getOpenFileName(self, self.tr("Choose OBJ file"), "", "OBJ Files (*.obj)")
        if filename:
            self.gl_widget.load_obj(filename)
