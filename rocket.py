
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math


rocket_x = 400
rocket_y = 100

speed = 0
launched = False
frame = 0


# Draw Rectangle
def rectangle(x1, y1, x2, y2, color):

    glColor3f(*color)

    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()


# Draw Triangle
def triangle(a, b, c, color):

    glColor3f(*color)

    glBegin(GL_TRIANGLES)
    glVertex2f(*a)
    glVertex2f(*b)
    glVertex2f(*c)
    glEnd()


# Draw Circle
def circle(x, y, radius, color):

    glColor3f(*color)

    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)

    for i in range(101):

        angle = 2 * math.pi * i / 100

        glVertex2f(
            x + radius * math.cos(angle),
            y + radius * math.sin(angle)
        )

    glEnd()


# Draw Rocket
def draw_rocket():

    global frame

    x = rocket_x
    y = rocket_y

    # Rocket Fire Animation
    if launched:

        flame = 30 + 10 * abs(math.sin(frame))

        triangle(
            (x - 12, y),
            (x + 12, y),
            (x, y - flame),
            (1.0, 0.3, 0.0)
        )

        triangle(
            (x - 6, y),
            (x + 6, y),
            (x, y - flame * 0.6),
            (1.0, 0.9, 0.0)
        )

    # Rocket Body
    rectangle(
        x - 20, y,
        x + 20, y + 100,
        (0.9, 0.9, 0.9)
    )

    # Rocket Head
    triangle(
        (x - 20, y + 100),
        (x + 20, y + 100),
        (x, y + 145),
        (0.9, 0.0, 0.0)
    )

    # Left Fin
    triangle(
        (x - 20, y + 25),
        (x - 40, y - 5),
        (x - 20, y - 5),
        (0.9, 0.0, 0.0)
    )

    # Right Fin
    triangle(
        (x + 20, y + 25),
        (x + 40, y - 5),
        (x + 20, y - 5),
        (0.9, 0.0, 0.0)
    )

    # Rocket Window
    circle(
        x, y + 75,
        11,
        (0.0, 0.5, 0.9)
    )


# Display Function
def display():

    glClearColor(0.5, 0.8, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # Ground
    rectangle(
        0, 0, 800, 60,
        (0.1, 0.5, 0.1)
    )

    # Launch Pad
    rectangle(
        320, 60, 480, 90,
        (0.3, 0.3, 0.3)
    )

    # Sun
    circle(
        700, 500, 35,
        (1.0, 0.9, 0.0)
    )

    # Rocket
    draw_rocket()

    # Title
    glColor3f(0, 0, 0)
    glRasterPos2f(260, 550)

    title = "2D ROCKET LAUNCH SIMULATOR"

    for ch in title:
        glutBitmapCharacter(
            GLUT_BITMAP_HELVETICA_18,
            ord(ch)
        )

    # Instructions and Status
    glRasterPos2f(220, 520)

    if not launched:

        message = "UP: Launch | LEFT/RIGHT: Move | DOWN: Reset"

    elif rocket_y > 600:

        message = "MISSION COMPLETE! | DOWN: Reset"

    else:

        message = "ROCKET LAUNCHING... | DOWN: Reset"

    for ch in message:
        glutBitmapCharacter(
            GLUT_BITMAP_HELVETICA_18,
            ord(ch)
        )

    glutSwapBuffers()


# Animation Update Function
def update(value):

    global rocket_y, speed, frame

    if launched and rocket_y <= 600:

        rocket_y += speed
        speed += 0.04
        frame += 0.25

    glutPostRedisplay()

    glutTimerFunc(16, update, 0)


# Arrow Key Controls
def special_keyboard(key, x, y):

    global rocket_x, rocket_y
    global speed, launched, frame

    # Move Rocket Left
    if key == GLUT_KEY_LEFT and not launched:

        rocket_x = max(300, rocket_x - 20)

    # Move Rocket Right
    elif key == GLUT_KEY_RIGHT and not launched:

        rocket_x = min(500, rocket_x + 20)

    # Launch Rocket
    elif key == GLUT_KEY_UP and not launched:

        launched = True
        speed = 2

    # Reset Rocket
    elif key == GLUT_KEY_DOWN:

        rocket_x = 400
        rocket_y = 100

        speed = 0
        launched = False
        frame = 0

    glutPostRedisplay()


# Window Reshape Function
def reshape(w, h):

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(0, 800, 0, 600, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# Main Function
glutInit()

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)

glutInitWindowSize(800, 600)
glutInitWindowPosition(100, 50)

glutCreateWindow(b"2D Rocket Launch Simulator")

glutDisplayFunc(display)

glutSpecialFunc(special_keyboard)

glutReshapeFunc(reshape)

glutTimerFunc(16, update, 0)

glutMainLoop()
