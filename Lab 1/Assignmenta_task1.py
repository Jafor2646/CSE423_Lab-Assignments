from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

win_w, win_h = 600, 600

rain_particles = []
for i in range(1000):
    rain_particles.append([random.randint(0, win_w), random.randint(0, win_h), 2, 18])

wind_offset = 0
fall_speed = 3
background_intensity = 0.85
brightness_step = 0.04

def draw_structure():
    #house base
    glColor3f(0.3, 0.2, 0.6)
    glBegin(GL_TRIANGLES)
    glVertex2d(150, 50)
    glVertex2d(150, 300)
    glVertex2d(450, 300)
    glEnd()

    glColor3f(0.3, 0.2, 0.6)
    glBegin(GL_TRIANGLES)
    glVertex2d(150, 50)
    glVertex2d(450, 50)
    glVertex2d(450, 300)
    glEnd()

    #Roof
    glColor3f(0, 0, 1)
    glBegin(GL_TRIANGLES)
    glVertex2d(150, 300)
    glVertex2d(300, 450)
    glVertex2d(450, 300)
    glEnd()
    
    #Door
    glColor3f(0.4, 0.2, 0.1)
    glBegin(GL_TRIANGLES)
    glVertex2d(250, 50)
    glVertex2d(250, 180)
    glVertex2d(350, 180)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2d(250, 50)
    glVertex2d(350, 50)
    glVertex2d(350, 180)
    glEnd()

    #Window
    glColor3f(0.1, 0.7, 0.9)
    glBegin(GL_TRIANGLES)
    glVertex2d(370, 200)
    glVertex2d(370, 270)
    glVertex2d(440, 270)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2d(370, 200)
    glVertex2d(440, 200)
    glVertex2d(440, 270)
    glEnd()

    #window crossbar
    glColor3f(0, 0, 0)
    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex2d(370, 235)
    glVertex2d(440, 235)
    glEnd()

    glBegin(GL_LINES)
    glVertex2d(405, 200)
    glVertex2d(405, 270)
    glEnd()

def draw_raindrops():
    global rain_particles, wind_offset
    for drop in rain_particles:
        glColor3f(0.4, 0.1, 1.0)
        glLineWidth(drop[2])
        glBegin(GL_LINES)
        glVertex2f(drop[0] - wind_offset, drop[1])
        glVertex2f(drop[0], drop[1] - drop[3])
        glEnd()

def keyboard_input(key, x, y):
    global background_intensity
    if key == b'd':
        if background_intensity < 0.85:
            background_intensity += brightness_step
    elif key == b'n':
        if background_intensity > 0.15:
            background_intensity -= brightness_step
    glutPostRedisplay()

def special_keys(key, x, y):
    global wind_offset
    if key == GLUT_KEY_LEFT: 
        wind_offset -= 1
    if key == GLUT_KEY_RIGHT:
        wind_offset += 1
    glutPostRedisplay()

def render_scene():
    global background_intensity
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(background_intensity, background_intensity, background_intensity, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_raindrops()
    draw_structure()

    glutSwapBuffers()

def animate():
    global rain_particles, win_w, win_h, fall_speed, wind_offset
    for drop in rain_particles:
        drop[1] = (drop[1] - fall_speed) % win_h
        drop[0] = (drop[0] + wind_offset) % win_w
    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, win_w, 0, win_h, -1, 1)

glutInit()
glutInitWindowSize(win_w, win_h)
glutInitWindowPosition(150, 150)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

win = glutCreateWindow(b"House with Rain")
init()

glutDisplayFunc(render_scene)
glutIdleFunc(animate)
glutKeyboardFunc(keyboard_input)
glutSpecialFunc(special_keys)

glutMainLoop()
