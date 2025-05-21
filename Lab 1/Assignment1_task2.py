from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

W_Width, W_Height = 500, 500
boundary = 200  

points = []  
speed_factor = 0.01  
blinking = False  
frozen = False 

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)  
        self.vy = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        self.r = random.random()
        self.g = random.random()
        self.b = random.random()
        self.blink_state = True  

    def move(self):
        if frozen:
            return

        self.x += self.vx * speed_factor
        self.y += self.vy * speed_factor

        if self.x >= boundary or self.x <= -boundary:
            self.vx *= -1  
        if self.y >= boundary or self.y <= -boundary:
            self.vy *= -1  

    def toggle_blink(self):
        if blinking:
            self.blink_state = not self.blink_state  

def draw_boundary():
    glColor3f(1, 1, 1)  
    glBegin(GL_LINES)

    # Bottom Edge
    glVertex2f(-boundary, -boundary)
    glVertex2f(boundary, -boundary)

    # Right Edge
    glVertex2f(boundary, -boundary)
    glVertex2f(boundary, boundary)

    # Top Edge
    glVertex2f(boundary, boundary)
    glVertex2f(-boundary, boundary)

    # Left Edge
    glVertex2f(-boundary, boundary)
    glVertex2f(-boundary, -boundary)

    glEnd()


def draw_points():
    for p in points:
        if blinking and not p.blink_state:
            continue  
        
        glColor3f(p.r, p.g, p.b)
        glPointSize(5)
        glBegin(GL_POINTS)
        glVertex2f(p.x, p.y)
        glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    draw_boundary() 
    draw_points()  

    glutSwapBuffers()

def animate():
    if not frozen:
        for p in points:
            p.move()
        if blinking:
            for p in points:
                p.toggle_blink()
    
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global frozen, speed_factor, blinking

    if key == b' ':  
        frozen = not frozen

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed_factor

    if frozen:
        return

    if key == GLUT_KEY_UP:  
        speed_factor *= 1.5
       

    elif key == GLUT_KEY_DOWN:  
        
        speed_factor /= 1.5

    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global blinking

    if frozen:
        return

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        gl_x = (x - W_Width / 2)  
        gl_y = (W_Height / 2 - y)  
        
        if -boundary <= gl_x and gl_x <= boundary and -boundary <= gl_y and gl_y <= boundary:
            new_point = Point(gl_x, gl_y)
            points.append(new_point)

    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blinking = not blinking

    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 1)  
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-W_Width / 2, W_Width / 2, -W_Height / 2, W_Height / 2)  
    glMatrixMode(GL_MODELVIEW)  

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"Task 2")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()
