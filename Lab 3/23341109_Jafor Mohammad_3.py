from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

window_width, window_height = 1000, 800
grid_dimension = 600
player_angle = 90
camera_tracking = False
cheat_mode = False
vision_cheat_mode = False
cheat_cycle = 0
camera_vertical_offset = 500
camera_horizontal_rotation = 0
view_angle = 120

player_coordinates = [0, 0]
player_lives = 5
missed_shots_count = 0
current_score = 0
active_projectiles = []
active_enemies = []
game_over_flag = False

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.z = 80
        self.angle = angle

    def update_position(self):
        self.x += 3 * math.cos(math.radians(self.angle - 90))
        self.y += 3 * math.sin(math.radians(self.angle - 90))

class Enemy:
    def __init__(self):
        self.reset_position()

    def reset_position(self):
        angle = random.uniform(0, 2 * math.pi)
        radius = 400
        self.x = radius * math.cos(angle)
        self.y = radius * math.sin(angle)
        self.z = 50
        self.size = 20
        self.is_increasing_size = True

    def approach_player(self):
        dx = player_coordinates[0] - self.x
        dy = player_coordinates[1] - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance > 1:
            self.x += dx / distance * 0.2
            self.y += dy / distance * 0.2

        if self.is_increasing_size:
            self.size += 0.5
            if self.size >= 30:
                self.is_increasing_size = False
        else:
            self.size -= 0.5
            if self.size <= 20:
                self.is_increasing_size = True

def draw_text(x, y, text):
    glColor3f(0.8, 0.8, 0.8)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def render_player():
    glPushMatrix()
    glTranslatef(player_coordinates[0], player_coordinates[1], 0)
    glRotatef(player_angle, 0, 0, 1)
    glRotatef(90, 1, 0, 0)
    glTranslatef(0, 0, 30)

    glColor3f(0.2, 0.2, 0.2)
    glTranslatef(0, 200, 0)
    gluSphere(gluNewQuadric(), 30, 20, 20)

    glTranslatef(0, -80, 0)
    glPushMatrix()
    glScalef(1, 1.2, 0.5)
    glColor3f(0.1, 0.5, 0.8)
    glutSolidCube(60)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-15, -100, 0)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.7, 0.3, 0.7)
    gluCylinder(gluNewQuadric(), 15, 7, 100, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(15, -100, 0)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.7, 0.3, 0.7)
    gluCylinder(gluNewQuadric(), 15, 7, 100, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-45, 10, 3)
    glRotatef(-90, 0, 0, 1)
    glColor3f(0.2, 0.8, 0.2)
    gluCylinder(gluNewQuadric(), 12, 6, 50, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(45, 10, 3)
    glRotatef(90, 0, 0, 1)
    glColor3f(0.2, 0.8, 0.2)
    gluCylinder(gluNewQuadric(), 12, 6, 50, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 10, 3)
    glColor3f(0.9, 0.1, 0.1)
    gluCylinder(gluNewQuadric(), 20, 10, 60, 20, 20)
    glPopMatrix()

    glPopMatrix()

def render_enemy(enemy):
    glPushMatrix()
    glTranslatef(enemy.x, enemy.y, 0)

    glColor3f(0.9, 0.1, 0.1)
    glutSolidSphere(50, 20, 20)

    glTranslatef(0, 0, 50)
    glColor3f(0.1, 0.1, 0.1)
    glutSolidSphere(30, 20, 20)

    glPopMatrix()

def render_bullet(bullet):
    glPushMatrix()
    glTranslatef(bullet.x, bullet.y, bullet.z)
    glColor3f(0.9, 0.9, 0.1)
    glutSolidCube(10)
    glPopMatrix()

def draw_game_grid():
    square_size = 40
    for x in range(-grid_dimension, grid_dimension, square_size):
        for y in range(-grid_dimension, grid_dimension, square_size):
            if (x // square_size + y // square_size) % 2 == 0:
                glColor3f(0.8, 0.8, 1.0)  # Light purple
            else:
                glColor3f(1.0, 1.0, 1.0)  # White
            glBegin(GL_QUADS)
            glVertex3f(x, y, 0)
            glVertex3f(x + square_size, y, 0)
            glVertex3f(x + square_size, y + square_size, 0)
            glVertex3f(x, y + square_size, 0)
            glEnd()

def draw_walls():
    wall_height = 100
    wall_thickness = 20

    # Left Wall
    glPushMatrix()
    glColor3f(0.0, 0.0, 1.0)  # Blue
    glTranslatef(-grid_dimension - wall_thickness / 2, 0, wall_height / 2)
    glScalef(wall_thickness, grid_dimension * 2, wall_height)
    glutSolidCube(1)
    glPopMatrix()

    # Right Wall
    glPushMatrix()
    glColor3f(0.0, 1.0, 0.0)  # Green
    glTranslatef(grid_dimension + wall_thickness / 2, 0, wall_height / 2)
    glScalef(wall_thickness, grid_dimension * 2, wall_height)
    glutSolidCube(1)
    glPopMatrix()

    # Top Wall
    glPushMatrix()
    glColor3f(0.0, 1.0, 1.0)  # Cyan
    glTranslatef(0, grid_dimension + wall_thickness / 2, wall_height / 2)
    glScalef(grid_dimension * 2, wall_thickness, wall_height)
    glutSolidCube(1)
    glPopMatrix()

    # Bottom Wall
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)  # Red
    glTranslatef(0, -grid_dimension - wall_thickness / 2, wall_height / 2)
    glScalef(grid_dimension * 2, wall_thickness, wall_height)
    glutSolidCube(1)
    glPopMatrix()

def render_scene():
    global active_projectiles, active_enemies, player_lives, missed_shots_count, current_score, game_over_flag

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, window_width, window_height)

    configure_camera()

    if game_over_flag:
        draw_text(400, 400, "GAME OVER! Press R to Restart")
        render_player()
        glutSwapBuffers()
        return

    draw_game_grid()
    draw_walls()
    render_player()

    new_projectiles = []
    for bullet in active_projectiles:
        bullet.update_position()
        if abs(bullet.x) > grid_dimension or abs(bullet.y) > grid_dimension:
            missed_shots_count += 1
            continue 
        hit = False
        for foe in active_enemies:
            dx = foe.x - bullet.x
            dy = foe.y - bullet.y
            distance = math.sqrt(dx * dx + dy * dy)
            if distance < foe.size:
                current_score += 1
                foe.reset_position()
                hit = True
                break
        if not hit:
            new_projectiles.append(bullet)
        render_bullet(bullet)

    active_projectiles = new_projectiles

    for enemy in active_enemies:
        enemy.approach_player()
        render_enemy(enemy)

    for enemy in active_enemies:
        dx = enemy.x - player_coordinates[0]
        dy = enemy.y - player_coordinates[1]
        if math.sqrt(dx ** 2 + dy ** 2) < enemy.size + 30:
            player_lives -= 1
            enemy.reset_position()

    if player_lives <= 0 or missed_shots_count >= 10:
        game_over_flag = True

    draw_text(10, 770, f"Life: {player_lives}  Score: {current_score}  Missed: {missed_shots_count}")

    glutSwapBuffers()

def keyboard_input(key, x, y):
    global player_coordinates, player_angle, cheat_mode, vision_cheat_mode, player_lives, current_score, missed_shots_count, active_projectiles, game_over_flag
    if game_over_flag and key == b'r':
        player_lives = 5
        missed_shots_count = 0
        current_score = 0
        active_projectiles.clear()
        for foe in active_enemies:
            foe.reset_position()
        game_over_flag = False
        cheat_mode = False
        player_coordinates = [0, 0]
        return

    if game_over_flag:
        return

    if key == b'w':
        player_coordinates[0] += 20 * math.cos(math.radians(player_angle - 90))
        player_coordinates[1] += 20 * math.sin(math.radians(player_angle - 90))
    if key == b's':
        player_coordinates[0] -= 20 * math.cos(math.radians(player_angle - 90))
        player_coordinates[1] -= 20 * math.sin(math.radians(player_angle - 90))
    if key == b'a':
        player_angle += 10
    if key == b'd':
        player_angle -= 10
    if key == b'c':
        cheat_mode = not cheat_mode
    if key == b'v':
        if camera_tracking:
            vision_cheat_mode = not vision_cheat_mode

def special_key_input(key, x, y):
    global camera_vertical_offset, camera_horizontal_rotation
    if key == GLUT_KEY_UP:
        camera_vertical_offset += 20
    elif key == GLUT_KEY_DOWN:
        camera_vertical_offset -= 20
    elif key == GLUT_KEY_LEFT:
        camera_horizontal_rotation -= 5
    elif key == GLUT_KEY_RIGHT:
        camera_horizontal_rotation += 5

def mouse_input(button, state, x, y):
    global camera_tracking
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        bullet_x = player_coordinates[0] + 30 * math.cos(math.radians(player_angle - 90))
        bullet_y = player_coordinates[1] + 30 * math.sin(math.radians(player_angle - 90))
        bullet_z = 80
        active_projectiles.append(Bullet(bullet_x, bullet_y, player_angle))
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_tracking = not camera_tracking

def fire_bullets_in_cheat_mode():
    global cheat_cycle
    if cheat_cycle % 500 == 0:
        for i in range(3):
            bullet_x = player_coordinates[0] + 10 * math.cos(math.radians(player_angle))
            bullet_y = player_coordinates[1] + 10 * math.sin(math.radians(player_angle))
            active_projectiles.append(Bullet(bullet_x, bullet_y, player_angle + i * 15 - 20))
    cheat_cycle += 1


def fire_bullets_in_cheat_mode_vision():
    global cheat_cycle
    if cheat_cycle % 500 == 0:
        for i in range(3):
            bullet_x = player_coordinates[0] + 10 * math.cos(math.radians(player_angle))
            bullet_y = player_coordinates[1] + 10 * math.sin(math.radians(player_angle))
            active_projectiles.append(Bullet(bullet_x, bullet_y, player_angle + i * 15 - 20))
    cheat_cycle += 1

def idle_function():
    global player_angle
    if cheat_mode and vision_cheat_mode:
        player_angle += 0.4
        fire_bullets_in_cheat_mode_vision()
    elif cheat_mode:
        player_angle += 0.2
        fire_bullets_in_cheat_mode()
    glutPostRedisplay()

def configure_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if camera_tracking and vision_cheat_mode and cheat_mode:
        gluPerspective(90, window_width / window_height, 1, 3000)
        cam_x = player_coordinates[0] + 220 * math.cos(math.radians(player_angle - 90))
        cam_y = player_coordinates[1] + 220 * math.sin(math.radians(player_angle - 90))
        cam_z = 100
        gluLookAt(-cam_x, -cam_y, cam_z, 
                  player_coordinates[0] + 200 * math.cos(math.radians(player_angle - 90)), 
                  player_coordinates[1] + 200 * math.sin(math.radians(player_angle - 90)), 
                  cam_z, 0, 0, 1)
    elif camera_tracking:
        gluPerspective(90, window_width / window_height, 1, 3000)
        cam_x = player_coordinates[0] + 100 * math.cos(math.radians(player_angle - 90))
        cam_y = player_coordinates[1] + 100 * math.sin(math.radians(player_angle - 90))
        cam_z = 100
        gluLookAt(cam_x, cam_y, cam_z, 
                  player_coordinates[0] + 200 * math.cos(math.radians(player_angle - 90)), 
                  player_coordinates[1] + 200 * math.sin(math.radians(player_angle - 90)), 
                  cam_z, 0, 0, 1)
    else:
        gluPerspective(view_angle, window_width / window_height, 1, 2000)
        cam_x = camera_vertical_offset * math.cos(math.radians(camera_horizontal_rotation))
        cam_y = camera_vertical_offset * math.sin(math.radians(camera_horizontal_rotation))
        gluLookAt(cam_x, cam_y, 500, 0, 0, 0, 0, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def initialize_game():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Bullet Frenzy")
    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(render_scene)
    glutKeyboardFunc(keyboard_input)
    glutSpecialFunc(special_key_input)
    glutMouseFunc(mouse_input)
    glutIdleFunc(idle_function)

    for _ in range(8):
        active_enemies.append(Enemy())

    glutMainLoop()

if __name__ == '__main__':
    initialize_game()
