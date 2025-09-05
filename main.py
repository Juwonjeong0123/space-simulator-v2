import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# 사용자 정의 모듈 임포트
from camera import Camera

# 윈도우 크기
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 카메라 객체 전역 변수
# 초기 위치: (0, 0, 5), 전방: (0, 0, -1), 위쪽: (0, 1, 0)
camera = Camera([0, 0, 5], [0, 0, -1], [0, 1, 0])

def handle_continuous_keyboard_input(window, delta_time):
    """
    렌더링 루프에서 매 프레임마다 키보드 입력을 처리합니다.
    """
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera.process_movement('W', delta_time)
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera.process_movement('S', delta_time)
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera.process_movement('A', delta_time)
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera.process_movement('D', delta_time)
    
    # 스페이스바 + 시프트로 위아래 이동
    is_shift_pressed = glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS or \
                       glfw.get_key(window, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS
    if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
        if is_shift_pressed:
            camera.process_movement('DOWN', delta_time)
        else:
            camera.process_movement('UP', delta_time)
            
    # 화살표 키 회전
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        camera.process_rotation('LEFT', delta_time)
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        camera.process_rotation('RIGHT', delta_time)
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        camera.process_rotation('UP', delta_time)
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        camera.process_rotation('DOWN', delta_time)

def draw_cube():
    """Renders a colorful cube."""
    vertices = np.array([
        [1, 1, -1], [-1, 1, -1], [-1, 1, 1], [1, 1, 1],
        [1, -1, 1], [-1, -1, 1], [-1, -1, -1], [1, -1, -1],
        [1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
        [1, -1, -1], [-1, -1, -1], [-1, 1, -1], [1, 1, -1],
        [1, -1, -1], [1, -1, 1], [1, 1, 1], [1, 1, -1],
        [-1, 1, -1], [-1, 1, 1], [-1, -1, 1], [-1, -1, -1]
    ], dtype=np.float32)

    colors = np.array([
        [1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1],
        [1, 1, 0, 1], [0, 1, 1, 1], [1, 0, 1, 1]
    ], dtype=np.float32)

    glBegin(GL_QUADS)
    for i in range(6):
        glColor4fv(colors[i])
        for j in range(4):
            index = i * 4 + j
            glVertex3fv(vertices[index])
    glEnd()

def draw_grid(size=20, divisions=20):
    """Renders a grid on the XZ plane."""
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)
    
    for i in range(divisions + 1):
        x = -size / 2 + i * (size / divisions)
        glVertex3f(x, 0, -size / 2)
        glVertex3f(x, 0, size / 2)

    for i in range(divisions + 1):
        z = -size / 2 + i * (size / divisions)
        glVertex3f(-size / 2, 0, z)
        glVertex3f(size / 2, 0, z)
    glEnd()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "PyOpenGL Modular Camera", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    
    glEnable(GL_DEPTH_TEST)
    camera.update_camera_vectors()
    
    last_frame_time = glfw.get_time()

    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        delta_time = current_time - last_frame_time
        last_frame_time = current_time
        
        handle_continuous_keyboard_input(window, delta_time)
        
        glfw.poll_events()
        
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        width, height = glfw.get_framebuffer_size(window)
        glViewport(0, 0, width, height)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 100)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        gluLookAt(
            camera.position[0], camera.position[1], camera.position[2],
            camera.position[0] + camera.front[0], camera.position[1] + camera.front[1], camera.position[2] + camera.front[2],
            camera.up[0], camera.up[1], camera.up[2]
        )
        
        draw_grid()
        
        time = glfw.get_time()
        glRotatef(time * 50, 0.5, 1, 0)
        
        draw_cube()
        
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
