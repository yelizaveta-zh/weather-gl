from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton
)

from gl.volume_widget import PyraWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.tr("PyQt6 OpenGL + Weather"))
        self._setup_ui()
        self._setup_timer()

    def _setup_ui(self):
        central = QWidget(self)
        layout = QHBoxLayout(central)

        self.gl_widget = PyraWidget(self)
        btn_reset = QPushButton(self.tr("Скинути позицію"))
        btn_reset.clicked.connect(self.gl_widget.reset_view)
        vbox_gl = QVBoxLayout()
        vbox_gl.addWidget(self.gl_widget)
        vbox_gl.addWidget(btn_reset)
