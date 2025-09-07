import numpy as np

class Camera:
    def __init__(self, position, front, up, yaw=-90.0, pitch=0.0, speed=0.05, sensitivity=0.25):
        self.position = np.array(position, dtype=np.float32)
        self.front = np.array(front, dtype=np.float32)
        self.up = np.array(up, dtype=np.float32)
        self.yaw = yaw
        self.pitch = pitch
        self.speed = speed
        self.sensitivity = sensitivity
        self.update_camera_vectors()

    def update_camera_vectors(self):
        """yaw와 pitch 값에 따라 카메라의 전방 벡터를 업데이트합니다."""
        front = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ], dtype=np.float32)
        
        self.front = front / np.linalg.norm(front)

    def process_movement(self, direction, delta_time):
        """
        카메라 이동을 처리합니다. deltaTime을 사용하여 부드러운 움직임을 구현합니다.
        direction: 'W', 'S', 'A', 'D', 'UP', 'DOWN'
        """
        speed = self.speed * delta_time * 100.0  # 속도를 프레임 간 시간에 맞춰 보정
        
        # 전방 벡터에서 수직 성분(Y축)을 제거하여 수평 이동을 만듭니다.
        horizontal_front = np.array([self.front[0], 0, self.front[2]])
        horizontal_front = horizontal_front / np.linalg.norm(horizontal_front)

        if direction == 'W':
            self.position += speed * horizontal_front
        elif direction == 'S':
            self.position -= speed * horizontal_front
        elif direction == 'A':
            self.position -= np.cross(self.front, self.up) * speed
        elif direction == 'D':
            self.position += np.cross(self.front, self.up) * speed
        elif direction == 'UP': # 위로 이동
            self.position += self.up * speed
        elif direction == 'DOWN': # 아래로 이동
            self.position -= self.up * speed
    
    def process_rotation(self, direction, delta_time):
        """
        카메라 회전을 처리합니다. deltaTime을 사용하여 부드러운 회전을 구현합니다.
        direction: 'UP', 'DOWN', 'LEFT', 'RIGHT'
        """
        rotation_speed = self.sensitivity * delta_time * 100.0
        
        if direction == 'UP':
            self.pitch += rotation_speed
            if self.pitch > 89.0: self.pitch = 89.0
        elif direction == 'DOWN':
            self.pitch -= rotation_speed
            if self.pitch < -89.0: self.pitch = -89.0
        elif direction == 'LEFT':
            self.yaw -= rotation_speed
        elif direction == 'RIGHT':
            self.yaw += rotation_speed

        self.update_camera_vectors()
