from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time

rain_drops = []
rain_angle = 0.0
rain_speed_multiplier = 1.0
background_color = [0.05, 0.05, 0.15]  # Night sky
target_background_color = [0.05, 0.05, 0.15]
day_factor = 0.0  # 0.0 = night, 1.0 = day
target_day_factor = 0.0
transition_speed = 0.001

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class RainDrop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(0.008, 0.015)
        self.length = random.uniform(0.03, 0.06)
        self.original_x = x
    
    def update(self):
        global rain_angle
        
        self.y -= self.speed
        
        self.x += rain_angle * 0.001
        
        if self.y < -1.2:
            self.y = 1.2
            self.x = random.uniform(-1.2, 1.2)
        
        if self.x > 1.2:
            self.x = -1.2
        elif self.x < -1.2:
            self.x = 1.2

def init():
    global background_color
    glClearColor(background_color[0], background_color[1], background_color[2], 1.0)
    glPointSize(5.0)
    glLineWidth(2.0)
    
    for i in range(100):
        x = random.uniform(-1.2, 1.2)
        y = random.uniform(-1.2, 1.2)
        rain_drops.append(RainDrop(x, y))

def lerp_color(color1, color2, factor):
    return [color1[0] * (1 - factor) + color2[0] * factor,
        color1[1] * (1 - factor) + color2[1] * factor,
        color1[2] * (1 - factor) + color2[2] * factor]

def interpolate_color(current, target, speed):
    new_color = []
    for i in range(3):
        if abs(current[i] - target[i]) < speed:
            new_color.append(target[i])
        elif current[i] < target[i]:
            new_color.append(current[i] + speed)
        else:
            new_color.append(current[i] - speed)
    return new_color

def draw_ground():
    # Ground color
    night_ground = [0.3, 0.2, 0.1]
    day_ground = [0.4, 0.3, 0.2]
    ground_color = lerp_color(night_ground, day_ground, day_factor)
    glColor3f(*ground_color)
    
    glBegin(GL_TRIANGLES)
    glVertex2f(-1.0, -0.4)
    glVertex2f(-1.0, -1.0)
    glVertex2f(1.0, -0.4)
    glVertex2f(1.0, -0.4)
    glVertex2f(-1.0, -1.0)
    glVertex2f(1.0, -1.0)
    glEnd()

    # Grass
    night_grass = [0.2, 0.6, 0.2]
    day_grass = [0.3, 0.9, 0.3]
    grass_color = lerp_color(night_grass, day_grass, day_factor)
    glColor3f(*grass_color)

    for i in range(27):
        x = -0.95 + i * 0.076
        wave_height = -0.32 + 0.02 * math.sin(i * 0.5)
        glBegin(GL_TRIANGLES)
        glVertex2f(x, -0.4)
        glVertex2f(x + 0.015, wave_height)
        glVertex2f(x + 0.03, -0.4)
        glEnd()

def draw_house():
    # House walls
    night_wall = [0.6, 0.55, 0.5]
    day_wall = [0.85, 0.8, 0.75]
    wall_color = lerp_color(night_wall, day_wall, day_factor)
    glColor3f(*wall_color)
    
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.45, -0.45)
    glVertex2f(-0.45, 0.15)
    glVertex2f(0.45, -0.45)
    glVertex2f(0.45, -0.45)
    glVertex2f(-0.45, 0.15)
    glVertex2f(0.45, 0.15)
    glEnd()
    
    # Chimney
    night_chimney = [0.35, 0.2, 0.15]
    day_chimney = [0.5, 0.3, 0.2]
    chimney_color = lerp_color(night_chimney, day_chimney, day_factor)
    glColor3f(*chimney_color)
    
    glBegin(GL_TRIANGLES)
    glVertex2f(0.25, 0.3)
    glVertex2f(0.25, 0.55)
    glVertex2f(0.35, 0.3)
    glVertex2f(0.35, 0.18)
    glVertex2f(0.25, 0.55)
    glVertex2f(0.35, 0.55)
    glEnd()
    
    # Chimney cap
    cap_color = [0.3, 0.3, 0.3]
    glColor3f(*cap_color)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.23, 0.55)
    glVertex2f(0.23, 0.58)
    glVertex2f(0.37, 0.55)
    glVertex2f(0.37, 0.55)
    glVertex2f(0.23, 0.58)
    glVertex2f(0.37, 0.58)
    glEnd()
    
    # Roof
    night_roof = [0.5, 0.15, 0.15]
    day_roof = [0.7, 0.2, 0.2]
    roof_color = lerp_color(night_roof, day_roof, day_factor)
    glColor3f(*roof_color)
    
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.55, 0.15)
    glVertex2f(0.0, 0.5)
    glVertex2f(0.55, 0.15)
    glEnd()
    
    # Roof ridge
    night_ridge = [0.6, 0.2, 0.2]
    day_ridge = [0.8, 0.3, 0.3]
    ridge_color = lerp_color(night_ridge, day_ridge, day_factor)
    glColor3f(*ridge_color)
    
    glLineWidth(1.5)
    glBegin(GL_LINES)
    glVertex2f(-0.55, 0.15)
    glVertex2f(0.55, 0.15)
    glEnd()
    glLineWidth(2.0)
    
    # Front door
    night_door = [0.25, 0.15, 0.08]
    day_door = [0.4, 0.2, 0.1]
    door_color = lerp_color(night_door, day_door, day_factor)
    glColor3f(*door_color)
    
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.1, -0.45)
    glVertex2f(-0.1, 0.05)
    glVertex2f(0.1, -0.45)
    glVertex2f(0.1, -0.45)
    glVertex2f(-0.1, 0.05)
    glVertex2f(0.1, 0.05)
    glEnd()
    
    # Door panels
    night_panel = [0.2, 0.1, 0.05]
    day_panel = [0.3, 0.15, 0.08]
    panel_color = lerp_color(night_panel, day_panel, day_factor)
    glColor3f(*panel_color)
    
    glBegin(GL_LINES)
    glVertex2f(-0.08, -0.1)
    glVertex2f(0.08, -0.1)
    glVertex2f(-0.08, -0.25)
    glVertex2f(0.08, -0.25)
    glEnd()

    # Door knob
    knob_color = [0.9, 0.8, 0.3]
    glColor3f(*knob_color)
    glPointSize(6.0)
    glBegin(GL_POINTS)
    glVertex2f(0.07, -0.2)
    glEnd()
    glPointSize(5.0)
    
    # Windows
    night_window = [0.3, 0.4, 0.6]
    day_window = [0.6, 0.8, 1.0]
    window_color = lerp_color(night_window, day_window, day_factor)
    glColor3f(*window_color)
    
    # Left window
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.35, -0.15)
    glVertex2f(-0.35, 0.05)
    glVertex2f(-0.18, -0.15)
    glVertex2f(-0.18, -0.15)
    glVertex2f(-0.35, 0.05)
    glVertex2f(-0.18, 0.05)
    glEnd()
    
    # Right window
    glBegin(GL_TRIANGLES)
    glVertex2f(0.18, -0.15)
    glVertex2f(0.18, 0.05)
    glVertex2f(0.35, -0.15)
    glVertex2f(0.35, -0.15)
    glVertex2f(0.18, 0.05)
    glVertex2f(0.35, 0.05)
    glEnd()
    
    # Window frames
    night_frame = [0.2, 0.15, 0.08]
    day_frame = [0.3, 0.2, 0.1]
    frame_color = lerp_color(night_frame, day_frame, day_factor)
    glColor3f(*frame_color)
    
    glLineWidth(3.0)
    glBegin(GL_LINES)

    # Left window frame
    glVertex2f(-0.35, -0.05)
    glVertex2f(-0.18, -0.05)
    glVertex2f(-0.265, -0.15)
    glVertex2f(-0.265, 0.05)

    # Right window frame
    glVertex2f(0.18, -0.05)
    glVertex2f(0.35, -0.05)
    glVertex2f(0.265, -0.15)
    glVertex2f(0.265, 0.05)
    glEnd()
    glLineWidth(2.0)
    
    # Window shutters
    night_shutter = [0.15, 0.25, 0.15]
    day_shutter = [0.2, 0.4, 0.2]
    shutter_color = lerp_color(night_shutter, day_shutter, day_factor)
    glColor3f(*shutter_color)
    
    glBegin(GL_TRIANGLES)

    # Left shutters
    glVertex2f(-0.42, -0.15)
    glVertex2f(-0.42, 0.05)
    glVertex2f(-0.37, -0.15)
    glVertex2f(-0.37, -0.15)
    glVertex2f(-0.42, 0.05)
    glVertex2f(-0.37, 0.05)
    glVertex2f(-0.16, -0.15)
    glVertex2f(-0.16, 0.05)
    glVertex2f(-0.11, -0.15)
    glVertex2f(-0.11, -0.15)
    glVertex2f(-0.16, 0.05)
    glVertex2f(-0.11, 0.05)

    # Right shutters
    glVertex2f(0.11, -0.15)
    glVertex2f(0.11, 0.05)
    glVertex2f(0.16, -0.15)
    glVertex2f(0.16, -0.15)
    glVertex2f(0.11, 0.05)
    glVertex2f(0.16, 0.05)
    glVertex2f(0.37, -0.15)
    glVertex2f(0.37, 0.05)
    glVertex2f(0.42, -0.15)
    glVertex2f(0.42, -0.15)
    glVertex2f(0.37, 0.05)
    glVertex2f(0.42, 0.05)
    glEnd()

#--> TREE DRAWING FUNCTION While Foliage is Not Static

# def draw_trees():
#     # Tree trunk
#     night_trunk = [0.3, 0.15, 0.08]
#     day_trunk = [0.4, 0.2, 0.1]
#     trunk_color = lerp_color(night_trunk, day_trunk, day_factor)
#     glColor3f(*trunk_color)
    
#     glBegin(GL_TRIANGLES)
#     # Left tree
#     glVertex2f(-0.82, -0.45)
#     glVertex2f(-0.82, -0.1)
#     glVertex2f(-0.78, -0.45)
#     glVertex2f(-0.78, -0.45)
#     glVertex2f(-0.82, -0.1)
#     glVertex2f(-0.78, -0.1)
    
#     # Right tree
#     glVertex2f(0.78, -0.45)
#     glVertex2f(0.78, -0.15)
#     glVertex2f(0.82, -0.45)
#     glVertex2f(0.82, -0.45)
#     glVertex2f(0.78, -0.15)
#     glVertex2f(0.82, -0.15)
#     glEnd()
    
#     # Tree foliage
#     night_foliage = [0.08, 0.4, 0.08]
#     day_foliage = [0.1, 0.6, 0.1]
#     foliage_color = lerp_color(night_foliage, day_foliage, day_factor)
#     glColor3f(*foliage_color)
    
#     glPointSize(12.0)
#     glBegin(GL_POINTS)
    
#     # Left tree foliage
#     for i in range(15):
#         angle = i * 24 * math.pi / 180
#         radius = 0.08 + random.uniform(-0.02, 0.02)
#         x = -0.8 + radius * math.cos(angle)
#         y = 0.0 + radius * math.sin(angle)
#         glVertex2f(x, y)

#     for i in range(15):
#         angle = i * 24 * math.pi / 180
#         radius = 0.09 + random.uniform(-0.02, 0.02)
#         x = -0.9 + radius * math.cos(angle)
#         y = 0.0 + radius * math.sin(angle)
#         glVertex2f(x, y)

#     for i in range(15):
#         angle = i * 24 * math.pi / 180
#         radius = 0.06 + random.uniform(-0.02, 0.02)
#         x = -0.8 + radius * math.cos(angle)
#         y = 0.1 + radius * math.sin(angle)
#         glVertex2f(x, y)

#     for i in range(15):
#         angle = i * 24 * math.pi / 180
#         radius = 0.06 + random.uniform(-0.02, 0.02)
#         x = -0.7 + radius * math.cos(angle)
#         y = 0.0 + radius * math.sin(angle)
#         glVertex2f(x, y)

#     # Right tree foliage
#     for i in range(12):
#         angle = i * 30 * math.pi / 180
#         radius = 0.07 + random.uniform(-0.015, 0.015)
#         x = 0.8 + radius * math.cos(angle)
#         y = -0.05 + radius * math.sin(angle)
#         glVertex2f(x, y)

#     for i in range(12):
#         angle = i * 30 * math.pi / 180
#         radius = 0.08 + random.uniform(-0.015, 0.015)
#         x = 0.9 + radius * math.cos(angle)
#         y = -0.05 + radius * math.sin(angle)
#         glVertex2f(x, y)

#     for i in range(12):
#         angle = i * 30 * math.pi / 180
#         radius = 0.05 + random.uniform(-0.015, 0.015)
#         x = 0.8 + radius * math.cos(angle)
#         y = 0.05 + radius * math.sin(angle)
#         glVertex2f(x, y)

#     for i in range(12):
#         angle = i * 30 * math.pi / 180
#         radius = 0.05 + random.uniform(-0.015, 0.015)
#         x = 0.7 + radius * math.cos(angle)
#         y = -0.05 + radius * math.sin(angle)
#         glVertex2f(x, y)

#     glEnd()
#     glPointSize(5.0)

def draw_trees():
    # Tree trunk
    night_trunk = [0.3, 0.15, 0.08]
    day_trunk = [0.4, 0.2, 0.1]
    trunk_color = lerp_color(night_trunk, day_trunk, day_factor)
    glColor3f(*trunk_color)
    
    glBegin(GL_TRIANGLES)
    # Left tree
    glVertex2f(-0.82, -0.45)
    glVertex2f(-0.82, -0.1)
    glVertex2f(-0.78, -0.45)
    glVertex2f(-0.78, -0.45)
    glVertex2f(-0.82, -0.1)
    glVertex2f(-0.78, -0.1)
    
    # Right tree
    glVertex2f(0.78, -0.45)
    glVertex2f(0.78, -0.15)
    glVertex2f(0.82, -0.45)
    glVertex2f(0.82, -0.45)
    glVertex2f(0.78, -0.15)
    glVertex2f(0.82, -0.15)
    glEnd()
    
    # Tree foliage
    night_foliage = [0.08, 0.4, 0.08]
    day_foliage = [0.1, 0.6, 0.1]
    foliage_color = lerp_color(night_foliage, day_foliage, day_factor)
    glColor3f(*foliage_color)
    
    glPointSize(12.0)
    glBegin(GL_POINTS)
    
    # Left tree foliage
    for i in range(15):
        angle = i * 24 * math.pi / 180
        radius = 0.08
        x = -0.8 + radius * math.cos(angle)
        y = 0.0 + radius * math.sin(angle)
        glVertex2f(x, y)

    for i in range(15):
        angle = i * 24 * math.pi / 180
        radius = 0.09
        x = -0.9 + radius * math.cos(angle)
        y = 0.0 + radius * math.sin(angle)
        glVertex2f(x, y)

    for i in range(15):
        angle = i * 24 * math.pi / 180
        radius = 0.06
        x = -0.8 + radius * math.cos(angle)
        y = 0.1 + radius * math.sin(angle)
        glVertex2f(x, y)

    for i in range(15):
        angle = i * 24 * math.pi / 180
        radius = 0.06
        x = -0.7 + radius * math.cos(angle)
        y = 0.0 + radius * math.sin(angle)
        glVertex2f(x, y)

    # Right tree foliage
    for i in range(12):
        angle = i * 30 * math.pi / 180
        radius = 0.07
        x = 0.8 + radius * math.cos(angle)
        y = -0.05 + radius * math.sin(angle)
        glVertex2f(x, y)

    for i in range(12):
        angle = i * 30 * math.pi / 180
        radius = 0.08
        x = 0.9 + radius * math.cos(angle)
        y = -0.05 + radius * math.sin(angle)
        glVertex2f(x, y)

    for i in range(12):
        angle = i * 30 * math.pi / 180
        radius = 0.05
        x = 0.8 + radius * math.cos(angle)
        y = 0.05 + radius * math.sin(angle)
        glVertex2f(x, y)

    for i in range(12):
        angle = i * 30 * math.pi / 180
        radius = 0.05
        x = 0.7 + radius * math.cos(angle)
        y = -0.05 + radius * math.sin(angle)
        glVertex2f(x, y)

    glEnd()
    glPointSize(5.0)

def draw_rain():
    night_rain = [0.4, 0.6, 0.8]
    day_rain = [0.6, 0.8, 1.0]
    rain_color = lerp_color(night_rain, day_rain, day_factor)
    glColor3f(*rain_color)
    
    angle_rad = math.radians(rain_angle)
    glBegin(GL_LINES)

    for drop in rain_drops:
        dx = drop.length * math.sin(angle_rad)
        dy = drop.length * math.cos(angle_rad)
        glVertex2f(drop.x - dx/2, drop.y + dy/2)
        glVertex2f(drop.x + dx/2, drop.y - dy/2)
    glEnd()

def draw_clouds():
    night_cloud = [0.05, 0.05, 0.15]
    day_cloud = [0.9, 0.9, 0.9]
    cloud_color = lerp_color(night_cloud, day_cloud, day_factor)
    glColor3f(*cloud_color)
    
    glPointSize(8.0)
    glBegin(GL_POINTS)

    # Cloud 1
    for i in range(15):
        x = -0.6 + (i % 5) * 0.03 + random.uniform(-0.01, 0.01)
        y = 0.85 + (i // 5) * 0.02 + random.uniform(-0.01, 0.01)
        glVertex2f(x, y)
    # Cloud 2
    for i in range(12):
        x = 0.6 + (i % 4) * 0.025 + random.uniform(-0.01, 0.01)
        y = 0.75 + (i // 4) * 0.02 + random.uniform(-0.01, 0.01)
        glVertex2f(x, y)
    # Cloud 3
    for i in range(9):
        x = -0.9 + (i % 5) * 0.04 + random.uniform(-0.01, 0.01)
        y = 0.5 + (i // 5) * 0.03 + random.uniform(-0.01, 0.01)
        glVertex2f(x, y)
    glEnd()
    glPointSize(5.0)

def draw_sun_moon():
    # Sun
    sun_color = [1.0, 1.0, 0.0]
    sun_intensity = day_factor
    glColor3f(sun_color[0] * sun_intensity, 
              sun_color[1] * sun_intensity, 
              sun_color[2] * sun_intensity)
    
    if sun_intensity > 0.1:
        glPointSize(18.0 * sun_intensity)
        glBegin(GL_POINTS)

        for i in range(20):
            angle = i * 18 * math.pi / 180
            x = 0.7 + 0.04 * math.cos(angle)
            y = 0.7 + 0.04 * math.sin(angle)
            glVertex2f(x, y)

        glEnd()
        
        # Sun rays
        glLineWidth(3.0 * sun_intensity)
        glBegin(GL_LINES)

        for i in range(8):
            angle = i * 45 * math.pi / 180
            x1 = 0.7 + 0.07 * math.cos(angle)
            y1 = 0.7 + 0.07 * math.sin(angle)
            x2 = 0.7 + 0.11 * math.cos(angle)
            y2 = 0.7 + 0.11 * math.sin(angle)
            glVertex2f(x1, y1)
            glVertex2f(x2, y2)

        glEnd()
        glLineWidth(2.0)
        glPointSize(5.0)

    # Moon and stars
    moon_color = [0.9, 0.9, 0.7]
    moon_intensity = 1.0 - day_factor

    if moon_intensity > 0.1:
        glColor3f(moon_color[0] * moon_intensity, 
                  moon_color[1] * moon_intensity, 
                  moon_color[2] * moon_intensity)
        
        glPointSize(8.0 * moon_intensity)
        glBegin(GL_POINTS)

        for i in range(20):
            angle = i * 18 * math.pi / 180
            x = -0.7 + 0.035 * math.cos(angle)
            y = 0.8 + 0.035 * math.sin(angle)
            glVertex2f(x, y)
        glEnd()
        
        # Moon craters
        crater_intensity = moon_intensity * 0.8
        glColor3f(0.7 * crater_intensity, 
                  0.7 * crater_intensity, 
                  0.5 * crater_intensity)
        glPointSize(3.0 * moon_intensity)

        glBegin(GL_POINTS)

        glVertex2f(-0.72, 0.82)
        glVertex2f(-0.68, 0.78)
        glVertex2f(-0.71, 0.77)
        glEnd()
        
        # Stars
        star_intensity = moon_intensity

        glColor3f(1.0 * star_intensity, 
                  1.0 * star_intensity, 
                  0.8 * star_intensity)
        glPointSize(3.0 * star_intensity)

        glBegin(GL_POINTS)

        star_positions = [(-0.3, 0.9), (0.2, 0.85), (0.6, 0.9), (-0.9, 0.7), 
            (0.8, 0.6), (-0.5, 0.5), (0.3, 0.4)]
        
        for x, y in star_positions:
            glVertex2f(x, y)

        glEnd()
        
        glPointSize(5.0)

def display():
    global background_color, target_background_color, day_factor
    
    if day_factor < target_day_factor:
        day_factor = min(day_factor + transition_speed, target_day_factor)

    elif day_factor > target_day_factor:
        day_factor = max(day_factor - transition_speed, target_day_factor)
    
    background_color = interpolate_color(background_color, target_background_color, transition_speed)
    glClearColor(background_color[0], background_color[1], background_color[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    draw_ground()
    draw_sun_moon()
    draw_clouds()
    draw_house()
    draw_rain()
    draw_trees()
    
    glutSwapBuffers()

def update():
    for drop in rain_drops:
        drop.update()
    glutPostRedisplay()

def keyboard(key, x, y):
    global target_background_color, target_day_factor
    
    key = key.decode('utf-8')
    
    if key == 'd':
        target_background_color = [0.5, 0.7, 1.0]
        target_day_factor = 1.0
        print("Transitioning to day-->")

    elif key == 'n':
        target_background_color = [0.05, 0.05, 0.15]
        target_day_factor = 0.0
        print("Transitioning to night-->")
        
    elif ord(key) == 27:
        exit(0)

def special_keys(key, x, y):
    global rain_angle, rain_speed_multiplier
    
    if key == GLUT_KEY_RIGHT:
        rain_angle = min(rain_angle + 2.0 * rain_speed_multiplier, 45.0)
        rain_speed_multiplier = min(rain_speed_multiplier + 0.1, 3.0)
        print(f"Rain angle: {rain_angle:.1f}°, Speed multiplier: {rain_speed_multiplier:.1f}")
        
    elif key == GLUT_KEY_LEFT:
        rain_angle = max(rain_angle - 2.0 * rain_speed_multiplier, -45.0)
        rain_speed_multiplier = min(rain_speed_multiplier + 0.1, 3.0)
        print(f"Rain angle: {rain_angle:.1f}°, Speed multiplier: {rain_speed_multiplier:.1f}")

def reshape(width, height):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    WINDOW_WIDTH = width
    WINDOW_HEIGHT = height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"23101137_Imtiaz Hossain_CSE423 Assignment 1 - Task 1: Building a House in Rainfall")
    
    init()
    
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutIdleFunc(update)
    
    glutMainLoop()

if __name__ == "__main__":
    main()