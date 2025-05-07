from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_LIGHT0,
    GL_LIGHTING,
    GL_POSITION,
    GL_PROJECTION,
    GL_MODELVIEW,
    GL_QUADS,
    GL_TRIANGLES,
    glBegin,
    glClear,
    glClearColor,
    glEnable,
    glEnd,
    glLightfv,
    glLoadIdentity,
    glMatrixMode,
    glNormal3f,
    glRotatef,
    glTranslatef,
    glVertex3f,
    glViewport,
)
from OpenGL.GLU import gluPerspective


def _draw_pyramid():
    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-1.0, -1.0, 0.0)
    glVertex3f(1.0, -1.0, 0.0)
    glVertex3f(1.0, 1.0, 0.0)
    glVertex3f(-1.0, 1.0, 0.0)
    glEnd()

    glBegin(GL_TRIANGLES)

    glNormal3f(0.0, -1.0, 0.707)
    glVertex3f(-1.0, -1.0, 0.0)
    glVertex3f(1.0, -1.0, 0.0)
    glVertex3f(0.0, 0.0, 1.2)

    glNormal3f(1.0, 0.0, 0.707)
    glVertex3f(1.0, -1.0, 0.0)
    glVertex3f(1.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 1.2)

    glNormal3f(0.0, 1.0, 0.707)
    glVertex3f(1.0, 1.0, 0.0)
    glVertex3f(-1.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 1.2)

    glNormal3f(-1.0, 0.0, 0.707)
    glVertex3f(-1.0, 1.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)
    glVertex3f(0.0, 0.0, 1.2)
    glEnd()


class PyraWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.x_rot = 0
        self.y_rot = 0
        self.distance = -5.0
        self.last_pos = QPoint()

    def initializeGL(self):
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 10, 1])

    def resizeGL(self, wght, hght):
        glViewport(0, 0, wght, hght)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = wght / hght if hght else 1
        gluPerspective(45.0, aspect, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, self.distance)
        glRotatef(self.x_rot / 16.0, 1, 0, 0)
        glRotatef(self.y_rot / 16.0, 0, 1, 0)
        _draw_pyramid()

    def mouse_press_event(self, event):
        self.last_pos = event.position().toPoint()

    def mouse_move_event(self, event):
        dx = event.position().x() - self.last_pos.x()
        dy = event.position().y() - self.last_pos.y()
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.x_rot += dy * 8
            self.y_rot += dx * 8
        self.last_pos = event.position().toPoint()
        self.update()

    def wheel_event(self, event):
        delta = event.angleDelta().y()
        self.distance += -delta / 240.0
        self.update()

    def reset_view(self):
        self.x_rot = 0
        self.y_rot = 0
        self.distance = -5.0
        self.update()
