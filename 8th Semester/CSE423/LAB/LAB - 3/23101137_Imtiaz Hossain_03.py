from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import math
import random
import sys


# ========================= Game Constants =========================

GRID_LENGTH = 90
GRID_SIZE = 17

PLAYER_SPEED = 20
CHEAT_SPEED = 50
BULLET_SPEED = 10
ENEMY_SPEED = 0.05

LEFT_BOUND = -GRID_SIZE * GRID_LENGTH // 2
RIGHT_BOUND = GRID_SIZE * GRID_LENGTH // 2

INITIAL_LIFE = 5

MAX_MISSED_BULLETS = 10
NUM_ENEMIES = 5

WINDOW_W = 1000
WINDOW_H = 700


# ========================= Game State =========================

camera_pos = (0, 500, 500)
fovY = 120
player_pos = [0, 0, 0]
player_angle = 0
camera_mode = "third"
game_over = False
bullets = []
enemies = []
life = INITIAL_LIFE
missed_bullets = 0
score = 0

prev_life = INITIAL_LIFE
prev_score = 0
prev_missed_bullets = 0
game_over_printed = False


# ========================= Cheat Mode State =========================

cheat_mode = False
auto_gun_following = False
can_fire = True
cheat_rotation = 0
cheat_cam_view = [-90, 30, 60]


# ========================= Terminal Output Functions =========================

def print_to_terminal(message):
    print(message)
    sys.stdout.flush()


def update_terminal_display(force=False):
    global prev_life, prev_score, prev_missed_bullets, game_over_printed
    
    if (force or life != prev_life or score != prev_score or 
        missed_bullets != prev_missed_bullets or game_over):
        
        if not game_over:
            if force:
                print_to_terminal("=== Bullet Frenzy Game ===")
                print_to_terminal(f"Remaining Player Life: {life}")
                print_to_terminal(f"Game Score: {score}")
                print_to_terminal(f"Player Bullet Missed: {missed_bullets}")
                print_to_terminal("")
            else:
                if life != prev_life:
                    print_to_terminal(f"Remaining Player Life: {life}")
                if score != prev_score:
                    print_to_terminal(f"Game Score: {score}")
                if missed_bullets != prev_missed_bullets:
                    print_to_terminal(f"Player Bullet Missed: {missed_bullets}")

        elif not game_over_printed:
            print_to_terminal("=== GAME OVER ===")
            print_to_terminal(f"Your final score is {score}.")
            print_to_terminal('Press "R" to RESTART the Game.')
            game_over_printed = True
        
        # Updating previous values
        prev_life = life
        prev_score = score
        prev_missed_bullets = missed_bullets


# ========================= Drawing Functions =========================

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_W, 0, WINDOW_H)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(font, ord(char))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_grid():
    half_size = GRID_SIZE // 2
    glBegin(GL_QUADS)
    
    for i in range(-half_size, half_size + 1):
        for j in range(-half_size, half_size + 1):
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)
                
            x_left = i * GRID_LENGTH
            x_right = (i + 1) * GRID_LENGTH
            y_bottom = j * GRID_LENGTH
            y_top = (j + 1) * GRID_LENGTH
            
            glVertex3f(x_left, y_bottom, 0)
            glVertex3f(x_right, y_bottom, 0)
            glVertex3f(x_right, y_top, 0)
            glVertex3f(x_left, y_top, 0)
    
    glEnd()


def draw_border_walls():
    wall_height = 120
    barricade = GRID_LENGTH * GRID_SIZE // 2
    
    glBegin(GL_QUADS)
    
    # Top wall
    glColor3f(1, 1, 1)
    glVertex3f(-barricade, barricade, 0)
    glVertex3f(barricade, barricade, 0)
    glVertex3f(barricade, barricade, wall_height)
    glVertex3f(-barricade, barricade, wall_height)
    
    # Right wall
    glColor3f(0.01, 0.9, 0.01)
    glVertex3f(barricade, -barricade, 0)
    glVertex3f(barricade, barricade, 0)
    glVertex3f(barricade, barricade, wall_height)
    glVertex3f(barricade, -barricade, wall_height)
    
    # Left wall
    glColor3f(0, 0, 1)
    glVertex3f(-barricade, -barricade, 0)
    glVertex3f(-barricade, barricade, 0)
    glVertex3f(-barricade, barricade, wall_height)
    glVertex3f(-barricade, -barricade, wall_height)
    
    # Bottom wall
    glColor3f(0.01, 0.9, 1)
    glVertex3f(-barricade, -barricade, 0)
    glVertex3f(barricade, -barricade, 0)
    glVertex3f(barricade, -barricade, wall_height)
    glVertex3f(-barricade, -barricade, wall_height)
    
    glEnd()


def draw_player():
    glPushMatrix()
    glTranslatef(*player_pos)
    glRotatef(player_angle, 0, 0, 1)
    
    if game_over:
        glRotatef(90, 0, 1, 0)
    
    # Left foot
    glColor3f(0, 0, 1)
    glTranslatef(0, -40, -100)
    glRotatef(90, 0, 1, 0)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 12, 6, 70, 10, 10)
    
    # Right foot
    glColor3f(0, 0, 1)
    glTranslatef(0, -90, 0)
    gluCylinder(gluNewQuadric(), 12, 6, 70, 10, 10)
    
    # Body
    glColor3f(0.4, 0.5, 0)
    glTranslatef(0, 40, -45)
    glutSolidCube(85)
    
    # Gun
    glColor3f(0.82, 0.82, 0.82)
    glTranslatef(0, 0, 40)
    glTranslatef(40, 0, -90)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 25, 10, 100, 10, 10)
    
    # Left Hand
    glColor3f(0.94, 0.75, 0.62)
    glTranslatef(0, -25, 0)
    gluCylinder(gluNewQuadric(), 15, 6, 60, 10, 10)
    
    # Right Hand
    glColor3f(0.94, 0.75, 0.62)
    glTranslatef(0, 50, 0)
    gluCylinder(gluNewQuadric(), 15, 6, 60, 10, 10)
    
    # Head
    glColor3f(0, 0, 0)
    glTranslatef(40, -25, -25)
    gluSphere(gluNewQuadric(), 35, 12, 10)
    
    glPopMatrix()


def draw_bullets():
    glColor3f(1, 0, 0)
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(*bullet['pos'])
        glutSolidCube(18)
        glPopMatrix()


def draw_enemy(enemy):
    glPushMatrix()
    glTranslatef(*enemy['pos'])
    
    # Body (Red)
    glColor3f(1, 0, 0)
    gluSphere(gluNewQuadric(), 40 * enemy["scale"], 20, 20)

    # Head (Black)
    glColor3f(0, 0, 0)
    glTranslatef(0, 0, 40)
    gluSphere(gluNewQuadric(), 30 * enemy["scale"], 20, 20)
    
    glPopMatrix()


# ========================= Game Mechanics =========================

def spawn_enemy():
    x = random.randint(LEFT_BOUND + 50, RIGHT_BOUND - 50)
    y = random.randint(LEFT_BOUND + 50, RIGHT_BOUND - 50)
    return {'pos': [x, y, 0], 'scale': 1.0, 'scale_dir': 0.005}


def initialize_enemies():
    global enemies
    enemies = []
    for _ in range(NUM_ENEMIES):
        enemies.append(spawn_enemy())


def fire_bullet(fire_pos=None, target_enemy=None):
    if fire_pos is None:  # Normal firing mode
        rad = math.radians(player_angle)
        dir_x = -math.cos(rad)
        dir_y = -math.sin(rad)
        
        gun_length = 150
        gun_right = 75
        gun_up = 12
        
        bullet_start = [player_pos[0] + gun_right * math.sin(rad) + dir_x * gun_length,
            player_pos[1] - gun_right * math.cos(rad) + dir_y * gun_length,
            player_pos[2] + gun_up]
        
        bullet_dir = [dir_x, dir_y, 0]
        print_to_terminal("Player Bullet Fired!")

    # Firing ---> Cheat Mode
    else:  
        dx = target_enemy["pos"][0] - fire_pos[0]
        dy = target_enemy["pos"][1] - fire_pos[1]
        dz = target_enemy["pos"][2] - fire_pos[2]
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        bullet_dir = [dx/dist, dy/dist, dz/dist]
        bullet_start = fire_pos.copy()
        print_to_terminal("Auto Bullet Fired! (Cheat Mode)")

    bullets.append({'pos': bullet_start, 'dir': bullet_dir})


def toggle_camera_mode():
    global camera_mode

    if camera_mode == "third":
        camera_mode = "first"

    else:
        camera_mode = "third"

    print_to_terminal(f"Camera mode: {camera_mode}")


def move_player(direction):
    global player_pos, cheat_cam_view
    
    angle = math.radians(player_angle)
    speed = CHEAT_SPEED if cheat_mode else PLAYER_SPEED
    move_x = -math.cos(angle) * speed if direction == 'w' else math.cos(angle) * speed
    move_y = -math.sin(angle) * speed if direction == 'w' else math.sin(angle) * speed
    
    new_x = player_pos[0] + move_x
    new_y = player_pos[1] + move_y
    
    if LEFT_BOUND <= new_x <= RIGHT_BOUND and LEFT_BOUND <= new_y <= RIGHT_BOUND:
        player_pos[0] = new_x
        player_pos[1] = new_y
        
        if camera_mode == "first" and cheat_mode and not auto_gun_following:
            cheat_cam_view[0] += move_x
            cheat_cam_view[1] += move_y


def rotate_player(direction):
    global player_angle
    angle_step = 4
    player_angle += angle_step if direction == 'a' else -angle_step


def toggle_cheat_mode():
    global cheat_mode, auto_gun_following
    cheat_mode = not cheat_mode
    auto_gun_following = False
    status = "ENABLED" if cheat_mode else "DISABLED"
    print_to_terminal(f"Cheat Mode {status}")


def toggle_automatic_gun_following():
    # Only allowing toggle in cheat mode
    global auto_gun_following
    
    if cheat_mode:
        auto_gun_following = not auto_gun_following
        status = "ENABLED" if auto_gun_following else "DISABLED"
        print_to_terminal(f"Auto Gun Following {status}")

    else:
        print_to_terminal("Auto Gun Following requires Cheat Mode to be enabled")


def restart_game():
    global game_over, player_pos, player_angle, life, score, missed_bullets, bullets
    global prev_life, prev_score, prev_missed_bullets, game_over_printed
    
    bullets.clear()
    initialize_enemies()
    
    score = 0
    missed_bullets = 0
    life = INITIAL_LIFE
    game_over = False
    player_pos[:] = [0, 0, 0]
    player_angle = 0
    
    # Reset tracking variables
    prev_life = INITIAL_LIFE
    prev_score = 0
    prev_missed_bullets = 0
    game_over_printed = False
    
    print_to_terminal("Game Restarted!")
    update_terminal_display(force=True)
    glutPostRedisplay()


# ========================= Input Handlers =========================

def mouse_listener(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        fire_bullet()  # Normal firing

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not game_over:
        toggle_camera_mode()

    glutPostRedisplay()


def keyboard_listener(key, x, y):
    if not game_over:
        if key == b'w' or key == b's':
            move_player('w' if key == b'w' else 's')
        elif key == b'a' or key == b'd':
            rotate_player('a' if key == b'a' else 'd')
        elif key == b"c":
            toggle_cheat_mode()
        elif key == b'v':
            toggle_automatic_gun_following()
    
    if key == b'r' and game_over:
        restart_game()


def special_key_listener(key, x, y):
    global camera_pos
    x, y, z = camera_pos
    
    if not game_over:
        if key == GLUT_KEY_UP:
            y += 1.5
        elif key == GLUT_KEY_DOWN:
            y -= 1.5
        elif key == GLUT_KEY_RIGHT:
            x += 1.5
        elif key == GLUT_KEY_LEFT:
            x -= 1.5
    
    camera_pos = (x, y, z)


# ========================= Camera Setup =========================

def setup_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, WINDOW_W / WINDOW_H, 0.2, 2000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if camera_mode == "third":
        setup_third_person_camera()
    elif camera_mode == "first":
        setup_first_person_camera()


def setup_third_person_camera():
    x, y, z = camera_pos
    gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)


def setup_first_person_camera():
    angle = math.radians(player_angle)
    
    if cheat_mode and auto_gun_following and camera_mode == "first":
        cam_pos = [player_pos[0] - 40,
            player_pos[1] + 35,
            player_pos[2] + 90]
        
        look_at = [player_pos[0],
            player_pos[1] + 200,
            player_pos[2]]
        
    else:
        # Normal first-person view from gun position
        cam_pos = [player_pos[0] + 40 * math.sin(angle) - math.cos(angle) * 60,
            player_pos[1] - 40 * math.cos(angle) - math.sin(angle) * 60,
            player_pos[2] + 40]
        
        # Normal first-person view direction
        look_at = [cam_pos[0] + (-math.cos(angle)) * 100,
            cam_pos[1] + (-math.sin(angle)) * 100,
            cam_pos[2]]
    
    gluLookAt(*cam_pos, *look_at, 0, 0, 1)


def find_nearest_enemy(position):
    if not enemies:
        return None
    
    nearest_enemy = None
    min_distance = float('inf')
    
    for enemy in enemies:
        dx = enemy["pos"][0] - position[0]
        dy = enemy["pos"][1] - position[1]
        dz = enemy["pos"][2] - position[2]
        distance = math.sqrt(dx*dx + dy*dy + dz*dz)
        
        if distance < min_distance:
            min_distance = distance
            nearest_enemy = enemy
    
    return nearest_enemy


# ========================= Game Logic =========================

def update_enemies():
    global life, game_over
    
    player_x, player_y, player_z = player_pos
    
    for enemy in enemies:
        # Enemy movement ---towards---> player
        diff_x = player_x - enemy['pos'][0]
        diff_y = player_y - enemy['pos'][1]
        dist_sq = diff_x * diff_x + diff_y * diff_y
        
        if dist_sq > 1:
            inv_dist = ENEMY_SPEED / math.sqrt(dist_sq)
            enemy['pos'][0] += diff_x * inv_dist
            enemy['pos'][1] += diff_y * inv_dist
        
        # Pulsing animation
        enemy['scale'] += enemy['scale_dir']
        if not 0.8 <= enemy['scale'] <= 1.2:
            enemy['scale_dir'] *= -1
            enemy['scale'] = min(max(enemy['scale'], 0.8), 1.2)
        
        # Collision detection with player
        if (not game_over and
                abs(player_x - enemy['pos'][0]) < 100 and
                abs(player_y - enemy['pos'][1]) < 100 and
                abs(player_z - enemy['pos'][2]) < 100):
            
            life -= 1
            enemies.remove(enemy)
            enemies.append(spawn_enemy())
            print_to_terminal(f"Player hit by enemy! Remaining Player Life: {life}")
            update_terminal_display()
            
            if life <= 0:
                game_over = True
                enemies.clear()
                print_to_terminal("GAME OVER - Player defeated!")
                return


def update_bullets():
    global bullets, missed_bullets, game_over
    
    for bullet in bullets[:]:
        bullet['pos'][0] += bullet['dir'][0] * BULLET_SPEED
        bullet['pos'][1] += bullet['dir'][1] * BULLET_SPEED
        bullet['pos'][2] += bullet['dir'][2] * BULLET_SPEED
        
        if (abs(bullet['pos'][0]) > 800 or
                abs(bullet['pos'][1]) > 800 or
                bullet['pos'][2] > 800 or
                bullet['pos'][2] < 0):
            bullets.remove(bullet)
            missed_bullets += 1
            print_to_terminal(f"Bullet missed: {missed_bullets}")
            update_terminal_display()
    
    if missed_bullets >= MAX_MISSED_BULLETS and not game_over:
        game_over = True
        enemies.clear()
        print_to_terminal("GAME OVER - Too many missed bullets!")

    elif life == 0 and not game_over:
        game_over = True
        enemies.clear()
        print_to_terminal("GAME OVER - Player defeated!")


def check_bullet_hits():
    global bullets, score
    
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if check_collision(bullet, enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                enemies.append(spawn_enemy())
                score += 1
                print_to_terminal(f"Enemy hit! Score: {score}")
                update_terminal_display()
                break


def check_collision(bullet, enemy):
    bx, by, bz = bullet['pos']
    ex, ey, ez = enemy['pos']
    return ((bx - ex) ** 2 + (by - ey) ** 2 + (bz - ez) ** 2) < 2500  # 50 units radius


def cheat_mode_actions():
    global player_angle, cheat_rotation, can_fire
    
    if not (cheat_mode and not game_over):
        return
    
    rotate_speed = 0.1
    player_angle = (player_angle + rotate_speed) % 360
    cheat_rotation += rotate_speed
    
    if cheat_rotation >= 30:
        cheat_rotation = 0
        can_fire = True
    
    if not can_fire:
        glutPostRedisplay()
        return
    
    # Gun direction vector
    rad = math.radians(player_angle)
    gun_dir_x = -math.cos(rad)
    gun_dir_y = -math.sin(rad)
    
    # Firing position from the gun
    gun_length = 150
    gun_right = 75
    gun_up = 12
    
    fire_pos = [
        player_pos[0] + gun_right * math.sin(rad) + gun_dir_x * gun_length,
        player_pos[1] - gun_right * math.cos(rad) + gun_dir_y * gun_length,
        player_pos[2] + gun_up
    ]
    
    for enemy in enemies:
        dx = enemy["pos"][0] - fire_pos[0]
        dy = enemy["pos"][1] - fire_pos[1]
        
        dot_product = dx * gun_dir_x + dy * gun_dir_y
        
        if dot_product > 0:
            dist_xy = math.sqrt(dx*dx + dy*dy)
            
            if dist_xy > 0:
                dir_to_enemy_x = dx / dist_xy
                dir_to_enemy_y = dy / dist_xy
                
                cos_angle = gun_dir_x * dir_to_enemy_x + gun_dir_y * dir_to_enemy_y
                
                if cos_angle > 0.995:
                    fire_bullet(fire_pos, enemy)
                    can_fire = False
                    break
    
    glutPostRedisplay()


def idle():
    update_bullets()
    check_bullet_hits()
    update_enemies()
    cheat_mode_actions()
    update_terminal_display()
    glutPostRedisplay()


# ========================= Window / Projection =========================

def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WINDOW_W, WINDOW_H)
    
    setup_camera()
    
    draw_grid()
    draw_border_walls()
    
    if not game_over:
        draw_text(10, 450, f"Player Life Remaining: {life}")
        draw_text(10, 430, f"Game Score: {score}")
        draw_text(10, 410, f"Player Bullet Missed: {missed_bullets}")
    else:
        draw_text(10, 460, f"Game is Over. Your score now is {score}.")
        draw_text(10, 440, 'Press "R" to RESTART the Game.')
    
    draw_player()
    draw_bullets()
    for enemy in enemies:
        draw_enemy(enemy)
    
    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 700)
    glutInitWindowPosition(150, 0)
    glutCreateWindow(b"23101137_Imtiaz Hossain____<Bullet Frenzy>")
    
    glutDisplayFunc(show_screen)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)
    glutIdleFunc(idle)
    
    initialize_enemies()
    print_to_terminal("=== 23101137_Imtiaz Hossain_Bullet Frenzy Game Started ===")
    update_terminal_display(force=True)
    
    glutMainLoop()


if __name__ == "__main__":
    main()