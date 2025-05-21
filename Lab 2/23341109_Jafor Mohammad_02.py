from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import random


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

STATE_RUNNING = 0
STATE_PAUSED = 1
STATE_GAME_OVER = 2

state = STATE_RUNNING
score = 0

diamond_size = 15
diamond_x = random.randint(diamond_size, WINDOW_WIDTH - diamond_size)
diamond_y = WINDOW_HEIGHT - diamond_size
diamond_speed = 100.0  
diamond_acceleration = 5.0
diamond_color = (random.random(), random.random(), random.random())

catcher_width = 100
catcher_height = 20
catcher_x = (WINDOW_WIDTH - catcher_width) // 2
catcher_y = 50

restart_btn = {"x": 20, "y": WINDOW_HEIGHT - 70, "width": 60, "height": 60}
playpause_btn = {"x": WINDOW_WIDTH // 2 - 30, "y": WINDOW_HEIGHT - 70, "width": 60, "height": 60}
exit_btn = {"x": WINDOW_WIDTH - 80, "y": WINDOW_HEIGHT - 70, "width": 60, "height": 60}

last_time = time.time()
print(last_time)
def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx > 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:  # dx > 0 and dy < 0:
            return 7
    else:
        if dx >= 0 and dy > 0:
            return 1
        elif dx < 0 and dy > 0:
            return 2
        elif dx < 0 and dy <= 0:
            return 5
        else:  
            return 6

def to_zone_0(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return y, -x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return -y, x
    if zone == 7: return x, -y

def from_zone_0(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return -y, x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return y, -x
    if zone == 7: return x, -y

def drawLine(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1p, y1p = to_zone_0(x1, y1, zone)
    x2p, y2p = to_zone_0(x2, y2, zone)

    dx = x2p - x1p
    dy = y2p - y1p
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    x = x1p
    y = y1p

    while x <= x2p:
        rx, ry = from_zone_0(x, y, zone)
        glBegin(GL_POINTS)
        glVertex2i(int(rx), int(ry))
        glEnd()
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1

def drawDiamond(cx, cy, size):
    drawLine(cx, cy + size, cx + size, cy)
    drawLine(cx + size, cy, cx, cy - size)
    drawLine(cx, cy - size, cx - size, cy)
    drawLine(cx - size, cy, cx, cy + size)

def drawCatcher(x, y, width, height):
    drawLine(x, y, x + width, y)
    drawLine(x + width, y, x + width, y + height)
    drawLine(x + width, y + height, x, y + height)
    drawLine(x, y + height, x, y)

def drawLeftArrow(x, y, size):
    drawLine(x + size, y + size, x, y)
    drawLine(x, y, x + size, y - size)

def drawPlayIcon(x, y, size):
    drawLine(x, y, x, y + size)
    drawLine(x, y + size, x + size, y + size // 2)
    drawLine(x + size, y + size // 2, x, y)

def drawPauseIcon(x, y, size):
    barWidth = size // 4
    barHeight = size
    lx = x
    ly = y - barHeight // 2
    drawCatcher(lx, ly, barWidth, barHeight)
    rx = x + barWidth * 2
    drawCatcher(rx, ly, barWidth, barHeight)

def drawCross(x, y, size):
    half = size // 2
    drawLine(x - half, y - half, x + half, y + half)
    drawLine(x - half, y + half, x + half, y - half)

def aabb_collision(box1, box2):
    return (box1[0] < box2[0] + box2[2] and box1[0] + box1[2] > box2[0] and box1[1] < box2[1] + box2[3] and box1[1] + box1[3] > box2[1])

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    if state == STATE_GAME_OVER:
        glColor3f(1.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)
    drawCatcher(catcher_x, catcher_y, catcher_width, catcher_height)
    
    glColor3f(diamond_color[0], diamond_color[1], diamond_color[2])
    drawDiamond(diamond_x, diamond_y, diamond_size)
    
    glColor3f(0.0, 0.8, 0.8)
    drawLeftArrow(restart_btn["x"] + 10, restart_btn["y"] + 30, 20)
    
    glColor3f(1.0, 0.65, 0.0)  
    if state == STATE_PAUSED:
        drawPlayIcon(playpause_btn["x"] + 10, playpause_btn["y"] + 10, 40)
    else:
        drawPauseIcon(playpause_btn["x"] + 10, playpause_btn["y"] + 30, 30)
    
    glColor3f(1.0, 0.0, 0.0)
    drawCross(exit_btn["x"] + 30, exit_btn["y"] + 30, 40)
    
    glFlush()
    glutSwapBuffers()

def timer(value):
    global last_time, diamond_y, diamond_speed, score, state, diamond_x, diamond_color, last_time

    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    if state == STATE_RUNNING:
        diamond_y -= diamond_speed * dt
        diamond_speed += diamond_acceleration * dt
        
        diamond_box = (diamond_x - diamond_size, diamond_y - diamond_size, diamond_size * 2, diamond_size * 2)
        catcher_box = (catcher_x, catcher_y, catcher_width, catcher_height)
        
        if aabb_collision(diamond_box, catcher_box):
            score += 1
            print("Score:", score)
            reset_diamond()
        
        if diamond_y - diamond_size < 0:
            state = STATE_GAME_OVER
            print("Game Over. Final Score:", score)
    
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0) 

def reset_diamond():
    global diamond_x, diamond_y, diamond_speed, diamond_color
    diamond_x = random.randint(diamond_size, WINDOW_WIDTH - diamond_size)
    diamond_y = WINDOW_HEIGHT - diamond_size
    diamond_speed = 100.0
    diamond_color = (random.random(), random.random(), random.random())

def keyboardSpecial(key, x, y):
    global catcher_x
    if state in (STATE_RUNNING, STATE_PAUSED):
        if key == GLUT_KEY_LEFT:
            catcher_x = max(0, catcher_x - 20)
        elif key == GLUT_KEY_RIGHT:
            catcher_x = min(WINDOW_WIDTH - catcher_width, catcher_x + 20)
    glutPostRedisplay()

def mouseFunc(button, state_click, x, y):
    global state, score, catcher_x, diamond_color, diamond_y, diamond_speed
    my = WINDOW_HEIGHT - y
    mx = x

    if (restart_btn["x"] <= mx <= restart_btn["x"] + restart_btn["width"] and restart_btn["y"] <= my <= restart_btn["y"] + restart_btn["height"]):
        print("Starting Over")
        reset_catcher()
        score = 0
        state = STATE_RUNNING
        reset_diamond()
    
    elif (playpause_btn["x"] <= mx <= playpause_btn["x"] + playpause_btn["width"] and playpause_btn["y"] <= my <= playpause_btn["y"] + playpause_btn["height"]):
        if state == STATE_RUNNING:
            state = STATE_PAUSED
            print("Game Paused")
        elif state == STATE_PAUSED:
            state = STATE_RUNNING
            print("Game Resumed")
    
    elif (exit_btn["x"] <= mx <= exit_btn["x"] + exit_btn["width"] and exit_btn["y"] <= my <= exit_btn["y"] + exit_btn["height"]):
        print("Goodbye. Final Score:", score)
        glutLeaveMainLoop()  
    
    glutPostRedisplay()

def reset_catcher():
    global catcher_x
    catcher_x = (WINDOW_WIDTH - catcher_width) // 2

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

last_time = time.time()
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Catch the Diamonds")
init()
glutDisplayFunc(display)
glutSpecialFunc(keyboardSpecial)
glutMouseFunc(mouseFunc)
glutTimerFunc(16, timer, 0)
glutMainLoop()
