from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


px=0
py=100
speed = 0.01
flag = 0
def upd():
    global px,py, speed, flag
    if(flag == 0):
        px=(px+speed)%500
    elif(flag == 1):
        px=(px-speed)%500
    elif(flag == 2):
        py=(py+speed)%500
    elif(flag == 3):
        py=(py-speed)%500
    glutPostRedisplay()

def kbd(key, x, y):
    global px,py,speed, flag
    
    if(key==b'w'):
        flag = 2
    if(key==b's'):
        flag = 3
    if(key==b'a'):
        flag = 1
    if(key==b'd'):
        flag = 0
    if(key == b'c'):
        speed = (speed + 0.02) %0.2
    if(key == b'x'):
        speed = (speed - 0.02) 
    glutPostRedisplay()

def draw_points(x, y):
    glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()

def draw_line(x, y,a,b):
    # glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_LINES)
    glVertex2f(x,y) #jekhane show korbe pixel
    glVertex2f(a,b) #jekhane show korbe pixel
    glEnd()


def draw_triangle(x, y, a, b, p, q):
    # glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_TRIANGLES)
    glVertex2f(x,y) #jekhane show korbe pixel
    glVertex2f(a,b) #jekhane show korbe pixel
    glVertex2f(p,q) #jekhane show korbe pixel
    glEnd()
def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)
    #call the draw methods here

    #draw_points(250, 250)

    # for i in range(100):
    #     draw_points(100+i, 100-i)   


    # #square
    # draw_line(200, 200, 300, 200)                                                                                                  
    # draw_line(200, 300, 300, 300)                                                                                                  
    # draw_line(200, 200, 200, 300)                                                                                                  
    # draw_line(300, 200, 300, 300)
    


    # # #triangle
    # draw_line(100, 350, 170, 420)
    # draw_line(240, 350, 170, 420)
    # draw_line(100, 350, 240, 350)
    
    
    # #triangle with function
    # draw_triangle(100,100,100,250,200,200)


    #animation
    draw_points(px, py)
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)
glutIdleFunc(upd)
glutKeyboardFunc(kbd)

glutMainLoop()





