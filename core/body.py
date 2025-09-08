import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

# -------------- icosphere 생성 함수 --------------
def normalize(v):
    return v / np.linalg.norm(v)

def create_icosphere(radius=1.0, subdivisions=0):
    t = (1.0 + np.sqrt(5.0)) / 2.0
    vertices = [
        (-1,  t,  0), ( 1,  t,  0), (-1, -t,  0), ( 1, -t,  0),
        ( 0, -1,  t), ( 0,  1,  t), ( 0, -1, -t), ( 0,  1, -t),
        ( t,  0, -1), ( t,  0,  1), (-t,  0, -1), (-t,  0,  1)
    ]
    vertices = [normalize(np.array(v)) * radius for v in vertices]

    faces = [
        (0,11,5), (0,5,1), (0,1,7), (0,7,10), (0,10,11),
        (1,5,9), (5,11,4), (11,10,2), (10,7,6), (7,1,8),
        (3,9,4), (3,4,2), (3,2,6), (3,6,8), (3,8,9),
        (4,9,5), (2,4,11), (6,2,10), (8,6,7), (9,8,1)
    ]

    # subdivision
    for _ in range(subdivisions):
        new_faces = []
        mid_cache = {}
        def get_midpoint(i1, i2):
            key = tuple(sorted((i1, i2)))
            if key in mid_cache:
                return mid_cache[key]
            v1, v2 = vertices[i1], vertices[i2]
            mid = normalize((v1 + v2) / 2) * radius
            vertices.append(mid)
            idx = len(vertices) - 1
            mid_cache[key] = idx
            return idx
        for tri in faces:
            i0,i1,i2 = tri
            a = get_midpoint(i0,i1)
            b = get_midpoint(i1,i2)
            c = get_midpoint(i2,i0)
            new_faces += [(i0,a,c), (i1,b,a), (i2,c,b), (a,b,c)]
        faces = new_faces

    return np.array(vertices, dtype=np.float32), np.array(faces, dtype=np.uint32)

# -------------- Sphere 클래스 --------------
class Sphere:
    def __init__(self, radius, pos, subdivisions=0, color=(0.5,0.5,1.0,1.0)):
        self.radius = float(radius)
        self.x, self.y, self.z = pos
        self.color = color
        self.vertices, self.faces = create_icosphere(radius, subdivisions)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)

        glBegin(GL_TRIANGLES)
        glColor4fv(self.color)
        for face in self.faces:
            for idx in face:
                glVertex3fv(self.vertices[idx])
        glEnd()

        glPopMatrix()

