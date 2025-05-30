import logging

from PyQt6.QtCore import QThread, pyqtSignal
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


logger = logging.getLogger(__name__)


class ModelLoader(QThread):
    loaded = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, filepath: str):
        super().__init__()
        self.filepath = filepath

    def run(self):
        vertices, normals, faces = [], [], []
        try:
            with open(self.filepath, "r") as f:
                for idx, line in enumerate(f, 1):
                    parts = line.strip().split()
                    if not parts:
                        continue
                    if parts[0] == "v":
                        _, x, y, z = parts
                        vertices.append([float(x), float(y), float(z)])
                    elif parts[0] == "vn":
                        _, x, y, z = parts
                        normals.append([float(x), float(y), float(z)])
                    elif parts[0] == "f":
                        face = []
                        for part in parts[1:]:
                            vals = part.split("//")
                            vi = int(vals[0]) - 1
                            ni = int(vals[1]) - 1 if len(vals) > 1 else 0
                            face.append([vi, ni])
                        faces.append(face)
            logger.info(f"Model loaded: {self.filepath}, verts={len(vertices)}, faces={len(faces)}")
            self.loaded.emit(vertices, normals, faces)
        except Exception as e:
            logger.exception(f"Exception loading model: {e}")
            self.error.emit(str(e))


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
        for btn in [btn_reset, btn_color, btn_load]:
            vbox_gl.addWidget(btn)

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
        filename, _ = QFileDialog.getOpenFileName(
            self, self.tr("Choose OBJ file"), "", "OBJ Files (*.obj)"
        )
        if not filename:
            return
        self.loader = ModelLoader(filename)
        self.loader.loaded.connect(self.on_model_load)
        self.loader.error.connect(self.on_model_error)
        self.loader.start()

    def on_model_loaded(self, data):
        vertices, normals, faces = data
        self.gl_widget.set_model_data(vertices, normals, faces)
        self.gl_widget.upload_model_to_gpu()

    def on_model_error(self, message):
        logger.error(f"Failed to load model: {message}")
