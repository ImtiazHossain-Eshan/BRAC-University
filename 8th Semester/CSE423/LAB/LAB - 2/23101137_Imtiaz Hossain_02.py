from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import random
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

INITIAL_DIAMOND_SPEED = 50  # pixels/second
DIAMOND_ACCELERATION = 5    # pixels/second^2
CATCHER_SPEED = 600         # pixels/second
DIAMOND_SIZE = 15
CATCHER_LENGTH = 100
CATCHER_HEIGHT = 15
BUTTON_SIZE = 30

score = 0
game_over = False
paused = False

diamond_x, diamond_y = 0, SCREEN_HEIGHT
diamond_color = (1.0, 1.0, 1.0)

catcher_x = SCREEN_WIDTH // 2
diamond_speed = INITIAL_DIAMOND_SPEED
last_time = 0

restart_button = (50, SCREEN_HEIGHT - 50, BUTTON_SIZE)
play_button = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, BUTTON_SIZE)
exit_button = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50, BUTTON_SIZE)

# ====================== Midpoint Line Drawing Algorithm ====================== #

def find_zone(x1, y1, x2, y2):

    dx, dy = x2 - x1, y2 - y1

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0: 
            return 0
        elif dx < 0 and dy >= 0: 
            return 3
        elif dx < 0 and dy < 0: 
            return 4
        else: 
            return 7

    else:
        if dx >= 0 and dy >= 0: 
            return 1
        elif dx < 0 and dy >= 0: 
            return 2
        elif dx < 0 and dy < 0: 
            return 5
        else: 
            return 6

def to_zone0(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return y, -x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return -y, x
    if zone == 7: return x, -y

def from_zone0(x0, y0, zone):
    if zone == 0: return x0, y0
    if zone == 1: return y0, x0
    if zone == 2: return -y0, x0
    if zone == 3: return -x0, y0
    if zone == 4: return -x0, -y0
    if zone == 5: return -y0, -x0
    if zone == 6: return y0, -x0
    if zone == 7: return x0, -y0

def midpoint_line_zone0(x1, y1, x2, y2):
    
    points = []
    dx, dy = x2 - x1, y2 - y1
    d = 2 * dy - dx
    incE, incNE = 2 * dy, 2 * (dy - dx)
    x, y = x1, y1
    
    while x <= x2:
        points.append((x, y))

        if d > 0:
            d += incNE
            y += 1

        else:
            d += incE
        x += 1

    return points

def draw_line(x1, y1, x2, y2):

    if x1 == x2 and y1 == y2:
        glVertex2f(x1, y1)
        return
    
    zone = find_zone(x1, y1, x2, y2)
    x1_0, y1_0 = to_zone0(x1, y1, zone)
    x2_0, y2_0 = to_zone0(x2, y2, zone)
    
    if x1_0 > x2_0:
        x1_0, x2_0 = x2_0, x1_0
        y1_0, y2_0 = y2_0, y1_0
    
    points = midpoint_line_zone0(x1_0, y1_0, x2_0, y2_0)
    
    for x0, y0 in points:
        x, y = from_zone0(x0, y0, zone)
        glVertex2f(x, y)

# ======================== Game Drawing Functions =========================== #

def draw_diamond(cx, cy, size, color):

    glColor3f(*color)

    draw_line(cx, cy + size, cx + size, cy)  # Top --> right
    draw_line(cx + size, cy, cx, cy - size)   # Right --> bottom
    draw_line(cx, cy - size, cx - size, cy)   # Bottom --> left
    draw_line(cx - size, cy, cx, cy + size)   # Left --> top

def draw_catcher(cx, cy, length, height, color):

    glColor3f(*color)
    half_len = length // 2

    draw_line(cx - half_len, cy, cx - half_len, cy + height)
    draw_line(cx - half_len, cy + height, cx + half_len, cy + height)
    draw_line(cx + half_len, cy + height, cx + half_len, cy)
    draw_line(cx + half_len, cy, cx - half_len, cy)

def draw_restart_button():

    glColor3f(0, 1, 1)  # Teal
    cx, cy, size = restart_button


    draw_line(cx + size//2, cy - size//3, cx - size//2, cy - size//3)

    draw_line(cx - size//2, cy - size//3, cx - size//4, cy)
    draw_line(cx - size//2, cy - size//3, cx - size//4, cy - 2*size//3)

def draw_play_pause_button():

    cx, cy, size = play_button

    if paused:
        glColor3f(1, 0.75, 0)

        draw_line(cx - size//3, cy - size//3, cx + size//3, cy)
        draw_line(cx + size//3, cy, cx - size//3, cy + size//3)
        draw_line(cx - size//3, cy + size//3, cx - size//3, cy - size//3)

    else:
        glColor3f(1, 0.75, 0)
   
        draw_line(cx - size//3, cy - size//3, cx - size//3, cy + size//3)
        draw_line(cx + size//3, cy - size//3, cx + size//3, cy + size//3)

def draw_exit_button():

    glColor3f(1, 0, 0)  # Red
    cx, cy, size = exit_button

    draw_line(cx - size//2, cy - size//2, cx + size//2, cy + size//2)
    draw_line(cx + size//2, cy - size//2, cx - size//2, cy + size//2)

# ======================== Game Logic Functions ============================= #

def check_collision():

    d_left = diamond_x - DIAMOND_SIZE
    d_right = diamond_x + DIAMOND_SIZE
    d_top = diamond_y + DIAMOND_SIZE
    d_bottom = diamond_y - DIAMOND_SIZE
    
    c_left = catcher_x - CATCHER_LENGTH//2
    c_right = catcher_x + CATCHER_LENGTH//2
    c_top = CATCHER_HEIGHT
    c_bottom = 0
    
    return (d_left < c_right and d_right > c_left and
            d_top > c_bottom and d_bottom < c_top)

def new_diamond():

    global diamond_x, diamond_y, diamond_color
    diamond_x = random.randint(DIAMOND_SIZE, SCREEN_WIDTH - DIAMOND_SIZE)
    diamond_y = SCREEN_HEIGHT
    diamond_color = (random.random(), random.random(), random.random())

    max_val = max(diamond_color)

    if max_val < 0.7:
        idx = diamond_color.index(max_val)
        new_color = list(diamond_color)
        new_color[idx] = 0.8 + random.random() * 0.2
        diamond_color = tuple(new_color)

def reset_game():

    global score, game_over, paused, catcher_x, diamond_speed
    score = 0
    game_over = False
    paused = False
    catcher_x = SCREEN_WIDTH // 2
    diamond_speed = INITIAL_DIAMOND_SPEED
    new_diamond()
    print("Starting Over")

# ========================== OpenGL Functions =============================== #

def init():

    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
    reset_game()

def display():

    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(1.0)
    glBegin(GL_POINTS)
    
    # if not game_over and not paused:
    #     draw_diamond(diamond_x, diamond_y, DIAMOND_SIZE, diamond_color)

    if not game_over:
        draw_diamond(diamond_x, diamond_y, DIAMOND_SIZE, diamond_color)
        

    catcher_color = (1.0, 0, 0) if game_over else (1.0, 1.0, 1.0)
    draw_catcher(catcher_x, 0, CATCHER_LENGTH, CATCHER_HEIGHT, catcher_color)
    
    
    draw_restart_button()
    draw_play_pause_button()
    draw_exit_button()
    
    glEnd()
    glutSwapBuffers()


def idle():

    global diamond_y, diamond_speed, last_time, game_over, score
    
    current_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    delta_time = current_time - last_time if last_time else 0.016
    last_time = current_time
    
    if not paused and not game_over:

        diamond_y -= diamond_speed * delta_time
        
        diamond_speed += DIAMOND_ACCELERATION * delta_time
        
        if check_collision():
            score += 1
            print(f"Score: {score}")
            new_diamond()

        if diamond_y + DIAMOND_SIZE < 0:
            print(f"Game Over! Score: {score}")
            game_over = True
    
    glutPostRedisplay() #--> Screen Refresh

def keyboard(key, x, y):

    global catcher_x

    if key == GLUT_KEY_LEFT and not game_over and not paused:
        catcher_x = max(CATCHER_LENGTH // 2, catcher_x - CATCHER_SPEED * 0.016)

    elif key == GLUT_KEY_RIGHT and not game_over and not paused:
        catcher_x = min(SCREEN_WIDTH - CATCHER_LENGTH // 2, catcher_x + CATCHER_SPEED * 0.016)
    
    glutPostRedisplay()

def mouse(button, state, x, y):
    
    global paused

    if button != GLUT_LEFT_BUTTON or state != GLUT_DOWN:
        return

    y = SCREEN_HEIGHT - y

    rx, ry, rs = restart_button
    if (x - rx)**2 + (y - ry)**2 <= rs**2:
        reset_game()

    px, py, ps = play_button
    if (x - px)**2 + (y - py)**2 <= ps**2:
        paused = not paused
    
    ex, ey, es = exit_button
    if (x - ex)**2 + (y - ey)**2 <= es**2:
        print(f"Goodbye! Score: {score}")
        glutLeaveMainLoop()

# =============================== Main ====================================== #

def main():

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    glutCreateWindow(b"23101137_IMTIAZ HOSSAIN_Catch the Diamonds!")
    
    init()
    glutDisplayFunc(display)
    glutSpecialFunc(keyboard)
    glutMouseFunc(mouse)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":

    main()