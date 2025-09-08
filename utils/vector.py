

# Vector3
class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # 연산자 오버로딩
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar):
        if scalar == 0:
            raise ValueError("Cannot divide by zero.")
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def to_tuple(self):
        """Pygame 또는 OpenGL 렌더링을 위해 튜플 형태로 변환합니다."""
        return (self.x, self.y, self.z)

