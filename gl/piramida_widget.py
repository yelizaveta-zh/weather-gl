from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QColor
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
    glColor3f,
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


class PyraWidget(QOpenGLWidget):
    def __init__(self, parent=None, base_size=1.0, height=1.2):
        super().__init__(parent)
        self.base_size = base_size
        self.height = height
        self.x_rot = 0
        self.y_rot = 0
        self.distance = -5.0
        self.last_pos = QPoint()
        self.color = (1.0, 1.0, 1.0)

    def set_color(self, qcolor: QColor):
        r = qcolor.redF()
        g = qcolor.greenF()
        b = qcolor.blueF()
        self.color = (r, g, b)
        self.update()

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
        glColor3f(*self.color)
        self._draw_pyramid()

    def _draw_pyramid(self):
        s = self.base_size
        h = self.height

        glBegin(GL_QUADS)
        glNormal3f(0, 0, -1)
        glVertex3f(-s, -s, 0)
        glVertex3f(s, -s, 0)
        glVertex3f(s, s, 0)
        glVertex3f(-s, s, 0)
        glEnd()

        glBegin(GL_TRIANGLES)
        normals = [(0, -1, 1), (1, 0, 1), (0, 1, 1), (-1, 0, 1)]
        verts = [(-s, -s), (s, -s), (s, s), (-s, s)]
        for i in range(4):
            nx, ny, nz = normals[i]
            glNormal3f(nx, ny, nz)
            x1, y1 = verts[i]
            x2, y2 = verts[(i + 1) % 4]
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(0, 0, h)
        glEnd()

    def mousePressEvent(self, event):
        self.last_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        dx = event.position().x() - self.last_pos.x()
        dy = event.position().y() - self.last_pos.y()
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.x_rot += dy * 8
            self.y_rot += dx * 8
        self.last_pos = event.position().toPoint()
        self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.distance += -delta / 240.0
        self.update()

    def reset_view(self):
        self.x_rot = 0
        self.y_rot = 0
        self.distance = -5.0
        self.update()
