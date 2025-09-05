import math
import numpy as np

# ====================
# 상수
# ====================
G = 6.674e-11  # 중력 상수

# ====================
# 클래스
# ====================
class Vector3:
    """
    3D 공간의 벡터를 나타내는 클래스.
    벡터 연산을 지원하여 위치, 속도, 가속도 등을 표현하는 데 사용합니다.
    """
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def magnitude(self):
        """벡터의 크기(길이)를 계산합니다."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        """벡터를 단위 벡터(크기가 1인 벡터)로 정규화합니다."""
        mag = self.magnitude()
        if mag == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / mag, self.y / mag, self.z / mag)

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

class CelestialBody:
    """
    천체(행성, 별)의 물리적 속성을 정의하는 클래스.
    """
    def __init__(self, name, mass, radius, position, velocity, color):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.pos = position  # Vector3 객체
        self.v = velocity    # Vector3 객체
        self.color = color   # RGB 튜플

        self.positions = []  # 궤적을 저장할 리스트
        self.positions.append(self.pos.to_tuple())

class Simulator:
    """
    천체 시뮬레이션의 물리 연산을 총괄하는 클래스.
    만유인력 계산 및 물체의 상태 업데이트를 관리합니다.
    """
    def __init__(self, bodies):
        """
        :param bodies: CelestialBody 객체 리스트
        """
        self.bodies = bodies
        self.G = G  # 중력 상수

    def calculate_acceleration(self, body):
        """
        특정 천체에 작용하는 모든 중력 가속도를 계산합니다.
        """
        total_force_vector = Vector3(0, 0, 0)
        for other_body in self.bodies:
            if body is other_body:
                continue

            r_vec = other_body.pos - body.pos
            r_mag = r_vec.magnitude()

            if r_mag == 0:
                continue

            force_magnitude = (self.G * body.mass * other_body.mass) / (r_mag**2)
            unit_vector = r_vec.normalize()

            force_vector = unit_vector * force_magnitude
            total_force_vector = total_force_vector + force_vector

        return total_force_vector / body.mass

    def step_simulation(self, dt):
        """
        주어진 시간 간격(dt)만큼 시뮬레이션을 한 단계 진행합니다.
        모든 천체의 속도와 위치를 업데이트하고, 궤적을 기록합니다.
        """
        # 각 물체에 대한 가속도 계산
        accelerations = {body: self.calculate_acceleration(body) for body in self.bodies}

        # 모든 물체의 속도와 위치 업데이트
        for body in self.bodies:
            # 뉴턴의 운동 법칙(F=ma)에 따라 가속도를 이용해 속도 업데이트
            body.v = body.v + accelerations[body] * dt
            # 속도를 이용해 위치 업데이트
            body.pos = body.pos + body.v * dt
            # 궤적 기록
            body.positions.append(body.pos.to_tuple())

# ====================
# 사용 예시
# ====================
"""
if __name__ == '__main__':
    # 태양과 지구 객체 생성
    sun = CelestialBody('Sun', 1.989e30, 6.963e8, Vector3(0, 0, 0), Vector3(0, 0, 0), (255, 255, 0))
    earth = CelestialBody('Earth', 5.972e24, 6.371e6, Vector3(1.496e11, 0, 0), Vector3(0, 29783, 0), (0, 0, 255))
    
    # 시뮬레이터 초기화
    solar_system = Simulator([sun, earth])

    # 시뮬레이션 진행 (예: 하루(86400초) 단위로 365일 시뮬레이션)
    dt = 86400 # 1일
    for _ in range(365):
        solar_system.step_simulation(dt)

    # 결과 확인
    print(f"지구의 최종 위치: ({earth.pos.x:.2f}, {earth.pos.y:.2f}, {earth.pos.z:.2f})")
"""
