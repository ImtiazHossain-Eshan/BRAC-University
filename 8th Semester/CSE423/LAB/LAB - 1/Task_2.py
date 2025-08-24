from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

points = []
speed_multiplier = 1.0
is_frozen = False
is_blinking = False
last_blink_time = 0
blink_duration = 1.0

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

BOUNDARY_LEFT = -0.9
BOUNDARY_RIGHT = 0.9
BOUNDARY_TOP = 0.9
BOUNDARY_BOTTOM = -0.9

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.r = random.uniform(0.2, 1.0)
        self.g = random.uniform(0.2, 1.0)
        self.b = random.uniform(0.2, 1.0)

        self.orig_r = self.r
        self.orig_g = self.g
        self.orig_b = self.b

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        self.dx, self.dy = random.choice(directions)

        self.base_speed = random.uniform(0.00002, 0.00005)
        
    def update(self):
        if is_frozen:
            return
            
        self.x += self.dx * self.base_speed * speed_multiplier
        self.y += self.dy * self.base_speed * speed_multiplier
        
        if self.x <= BOUNDARY_LEFT or self.x >= BOUNDARY_RIGHT:
            self.dx = -self.dx

            if self.x <= BOUNDARY_LEFT:
                self.x = BOUNDARY_LEFT

            elif self.x >= BOUNDARY_RIGHT:
                self.x = BOUNDARY_RIGHT
                
        if self.y <= BOUNDARY_BOTTOM or self.y >= BOUNDARY_TOP:
            self.dy = -self.dy

            if self.y <= BOUNDARY_BOTTOM:
                self.y = BOUNDARY_BOTTOM

            elif self.y >= BOUNDARY_TOP:
                self.y = BOUNDARY_TOP
    
    def draw(self):
        glColor3f(self.r, self.g, self.b)
        glPointSize(8.0)
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()

def conv_coord(x, y):

    gl_x = (2.0 * x / WINDOW_WIDTH) - 1.0
    gl_y = 1.0 - (2.0 * y / WINDOW_HEIGHT)
    return gl_x, gl_y

def update_blinking():

    if not is_blinking:
        return
        
    current_time = time.time()
    elapsed_time = current_time - last_blink_time
    

    phase = (elapsed_time % blink_duration) / blink_duration
    if phase > 0.5:
        phase = 1.0 - phase
    phase *= 2.0  # Scale to 0-1
    

    for point in points:
        point.r = point.orig_r * phase
        point.g = point.orig_g * phase
        point.b = point.orig_b * phase

def draw_boundary():

    glColor3f(0.3, 0.3, 0.3)  # Gray color
    glLineWidth(2.0)
    glBegin(GL_LINES)

    # Top
    glVertex2f(BOUNDARY_LEFT, BOUNDARY_TOP)
    glVertex2f(BOUNDARY_RIGHT, BOUNDARY_TOP)
    # Bottom
    glVertex2f(BOUNDARY_LEFT, BOUNDARY_BOTTOM)
    glVertex2f(BOUNDARY_RIGHT, BOUNDARY_BOTTOM)
    # Left
    glVertex2f(BOUNDARY_LEFT, BOUNDARY_TOP)
    glVertex2f(BOUNDARY_LEFT, BOUNDARY_BOTTOM)
    # Right
    glVertex2f(BOUNDARY_RIGHT, BOUNDARY_TOP)
    glVertex2f(BOUNDARY_RIGHT, BOUNDARY_BOTTOM)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_boundary()
    update_blinking()
    
    for point in points:
        point.update()
        point.draw()
    
    glutSwapBuffers()

def mouse_click(button, state, x, y):
    global is_blinking, last_blink_time
    
    if state == GLUT_DOWN:
        gl_x, gl_y = conv_coord(x, y)
        
        if button == GLUT_RIGHT_BUTTON:

            if (BOUNDARY_LEFT <= gl_x <= BOUNDARY_RIGHT and 
                BOUNDARY_BOTTOM <= gl_y <= BOUNDARY_TOP):

                new_point = Point(gl_x, gl_y)
                points.append(new_point)
                
        elif button == GLUT_LEFT_BUTTON:

            is_blinking = not is_blinking
            last_blink_time = time.time()
            
            if not is_blinking:

                for point in points:
                    point.r = point.orig_r
                    point.g = point.orig_g
                    point.b = point.orig_b

def keyboard(key, x, y):
    global speed_multiplier, is_frozen
    
    if key == b' ':  # Spacebar
        is_frozen = not is_frozen

def special_keys(key, x, y):
    global speed_multiplier
    
    if not is_frozen:
    
        if key == GLUT_KEY_UP:
            speed_multiplier = min(speed_multiplier * 1.2, 10)
        elif key == GLUT_KEY_DOWN:
            speed_multiplier = max(speed_multiplier * 0.8, 0.1)

def idle():
    glutPostRedisplay()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Black background
    glEnable(GL_POINT_SMOOTH)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"23101137_Imtiaz Hossain_CSE423 Assignment 1 - Task 2: Building the Amazing Box")
    
    init()
    
    glutDisplayFunc(display)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutIdleFunc(idle)

    glutMainLoop()

if __name__ == "__main__":
    main()