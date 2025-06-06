import ctypes
import logging
import numpy as np

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from OpenGL.GL import (
    GL_AMBIENT_AND_DIFFUSE,
    GL_ARRAY_BUFFER,
    GL_COLOR_BUFFER_BIT,
    GL_COLOR_MATERIAL,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_FRONT_AND_BACK,
    GL_FLOAT,
    GL_ELEMENT_ARRAY_BUFFER,
    GL_LIGHT0,
    GL_LIGHTING,
    GL_POSITION,
    GL_PROJECTION,
    GL_MODELVIEW,
    GL_NORMAL_ARRAY,
    GL_QUADS,
    GL_STATIC_DRAW,
    GL_TRIANGLES,
    GL_VERTEX_ARRAY,
    GL_UNSIGNED_INT,
    glBegin,
    glBindBuffer,
    glBufferData,
    glClear,
    glClearColor,
    glColorMaterial,
    glColor3f,
    glDisableClientState,
    glDrawElements,
    glGenBuffers,
    glEnable,
    glEnableClientState,
    glEnd,
    glLightfv,
    glLoadIdentity,
    glMatrixMode,
    glNormalPointer,
    glNormal3f,
    glRotatef,
    glTranslatef,
    glVertex3f,
    glVertexPointer,
    glViewport,
)
from OpenGL.GLU import gluPerspective


logger = logging.getLogger(__name__)


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

        self.vertices = []
        self.normals = []
        self.faces = []

        self.vbo_vertices = None
        self.vbo_indices = None

    def set_model_data(self, vertices, normals, faces):
        self.vertices = vertices
        self.normals = normals
        self.faces = faces
        logger.info(f"Model data set: verts={len(vertices)}, faces={len(faces)}")

        if not self._validate_model_data():
            logger.error("Model data validation failed")
            return

        self.upload_model_to_gpu()
        self.update()

    def _validate_model_data(self):
        """Validate the model data format"""
        if not self.vertices or not self.faces:
            logger.error("Vertices or faces are empty")
            return False

        if len(self.vertices[0]) != 3:
            logger.error("Vertices must be 3D (x, y, z)")
            return False

        if self.normals and len(self.normals) != len(self.vertices):
            logger.error(f"Normals count ({len(self.normals)}) doesn't match vertices count ({len(self.vertices)})")
            return False

        return True

    def set_color(self, qcolor: QColor):
        self.color = (qcolor.redF(), qcolor.greenF(), qcolor.blueF())
        self.update()

    def initializeGL(self):
        try:
            glClearColor(0.1, 0.1, 0.1, 1.0)
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 10, 1])
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        except Exception as e:
            logger.exception(f"InitializeGL error: {e}")

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
        glTranslatef(0, -self.base_size * 0.5, self.distance)
        glRotatef(self.x_rot / 16.0, 1, 0, 0)
        glRotatef(self.y_rot / 16.0, 0, 1, 0)
        glColor3f(*self.color)

        if self.vbo_vertices and self.vbo_indices and self.vertices:
            self._render_with_vbo()
        else:
            self._draw_pyramid()

    def _render_with_vbo(self):
        try:
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo_vertices)
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 6 * 4, ctypes.c_void_p(0))

            if self.normals:
                glEnableClientState(GL_NORMAL_ARRAY)
                glNormalPointer(GL_FLOAT, 6 * 4, ctypes.c_void_p(3 * 4))

            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo_indices)
            glDrawElements(GL_TRIANGLES, len(self.faces) * 3, GL_UNSIGNED_INT, None)

            glDisableClientState(GL_VERTEX_ARRAY)
            if self.normals:
                glDisableClientState(GL_NORMAL_ARRAY)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        except Exception as e:
            logger.exception(f"VBO rendering error: {e}")

    def upload_model_to_gpu(self):
        try:
            if not self.vertices and not self.faces:
                logger.warning("No vertices or faces found")
                return

            verts = np.array(self.vertices, dtype=np.float32)

            if self.normals:
                norms = np.array(self.normals, dtype=np.float32)
            else:
                norms = self._generate_normals()

            data = np.empty(len(verts) * 6, dtype=np.float32)
            data[:, :3] = verts
            data[:, 3:] = norms
            data = data.flatten()

            idxs = []
            for face in self.faces:
                if isinstance(face[0], (list, tuple)) and len(face[0]) == 2:
                    for vi, _ in face:
                        idxs.append(vi)
                else:
                    for vi in face:
                        idxs.append(vi)

            idxs = np.array(idxs, dtype=np.uint32)

            max_idx = np.max(idxs) if len(idxs) > 0 else 0
            if max_idx >= len(self.vertices):
                logger.error(f"Face index {max_idx} exceeds vertex count {len(self.vertices)}")
                return

            self.vbo_vertices = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo_vertices)
            glBufferData(GL_ARRAY_BUFFER, data.nbytes, data, GL_STATIC_DRAW)

            self.vbo_indices = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo_indices)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, idxs.nbytes, idxs, GL_STATIC_DRAW)

            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

            logger.info(f"Uploaded model to GPU: {len(verts)} vertices, {len(idxs)//3} triangles")

        except Exception as e:
            logger.exception(f"Error uploading model to GPU: {e}")

    def _generate_normals(self):
        logger.info("Generating vertex normals")
        normals = np.zeros((len(self.vertices), 3), dtype=np.float32)

        for face in self.faces:
            if len(face) >= 3:
                if isinstance(face[0], (list, tuple)):
                    v_indices = [vi for vi, _ in face[:3]]
                else:
                    v_indices = face[:3]

                v0, v1, v2 = [self.vertices[i] for i in v_indices]
                edge1 = np.array(v1) - np.array(v0)
                edge2 = np.array(v2) - np.array(v0)
                face_normal = np.cross(edge1, edge2)

                norm = np.linalg.norm(face_normal)
                if norm > 0:
                    face_normal /= norm

                for vi in v_indices:
                    normals[vi] += face_normal

        for i in range(len(normals)):
            norm = np.linalg.norm(normals[i])
            if norm > 0:
                normals[i] /= norm
            else:
                normals[i] = [0, 0, 1]

        return normals

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
            norm = (nx*nx + ny*ny + nz*nz) ** 0.5
            glNormal3f(nx/norm, ny/norm, nz/norm)
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
        self.distance += delta / 240.0
        self.update()

    def reset_view(self):
        self.x_rot = 0
        self.y_rot = 0
        self.distance = -5.0
        self.update()
