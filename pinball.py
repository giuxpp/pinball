import pygame
import pymunk
import pymunk.pygame_util
import math

LOGS_ALLOWED = False

# Global variables
SCREEN_WIDTH = 800
running = True 
game_over = True
lkey_pressed, rkey_pressed = False, False
screen = None
space = None
draw_options = None
body_lbar = None
body_rbar = None
body_ball = None

# Ball parameters
ball_radius = None
center_x, center_y = 100, 100

# Bar parameters (shared)
bar_length = None  # Will be set in game_init
bar_width = 30
bar_color = (200, 200, 102)  # Mustard yellow color
bar_y_offset = None
bar_inc_init = 0.15
bar_inc_step = 0.00006

# Left Bar parameters
left_bar_angle_initial = -45
left_bar_angle = None
left_bar_inc = None

# Right Bar parameters
right_bar_angle_initial = 135
right_bar_angle = None
right_bar_inc = None

# Angle ranges for bars
lbar_ang_start = math.radians(45)
lbar_ang_end = math.radians(0)
rbar_ang_start = math.radians(135)
rbar_ang_end = math.radians(180)

def log(str): 
    if LOGS_ALLOWED: print(str)

def game_init():
    global screen, ball_radius, center_x, center_y
    global bar_length, left_bar_angle, left_bar_angle_initial
    global right_bar_angle, right_bar_angle_initial, bar_y_offset, game_over
    global left_bar_inc, right_bar_inc, bar_inc_init
    # Set ball parameters
    center_x, center_y = 150, 100
    ball_radius = screen.get_height() // 33
    # Set bar parameters
    bar_length = screen.get_width() // 2.85
    left_bar_inc = bar_inc_init
    right_bar_inc = bar_inc_init
    bar_y_offset = 250
    left_bar_angle = left_bar_angle_initial
    right_bar_angle = right_bar_angle_initial
    game_over = False
    create_ball()

def create_window():
    global screen, SCREEN_WIDTH
    screen_height = int(SCREEN_WIDTH * 1.5)
    screen = pygame.display.set_mode((SCREEN_WIDTH, screen_height))
    pygame.display.set_caption("-- Pinball game --")

def handle_events():
    global running, left_bar_angle, right_bar_angle
    global lkey_pressed, rkey_pressed, game_over
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_LEFT:
                lkey_pressed = True
                log("Left key pressed")
            if ev.key == pygame.K_RIGHT:
                rkey_pressed = True
                log("Right key pressed")
            if ev.key == pygame.K_RETURN and game_over:
                game_init()
                log("Game reset")
            if ev.key == pygame.K_ESCAPE:
                if game_over:
                    log("Game over, press ENTER to reset")
                    running = False
                else:
                    game_over = True
                    log("Game paused, press ENTER to reset")
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_LEFT:
                lkey_pressed = False
                log("Left key released")
            if ev.key == pygame.K_RIGHT:
                rkey_pressed = False
                log("Right key released")

def update_bars():
    global left_bar_angle, left_bar_angle_initial, right_bar_angle, right_bar_angle_initial
    global lkey_pressed, rkey_pressed, left_bar_inc, right_bar_inc, bar_inc_init, bar_inc_step
    global body_lbar, body_rbar
    # Update left bar angle
    if lkey_pressed:                        
        body_lbar.angle = max(lbar_ang_end, body_lbar.angle - left_bar_inc)
        left_bar_inc += bar_inc_step
    else:
        body_lbar.angle = min(lbar_ang_start, body_lbar.angle + left_bar_inc)
        if body_lbar.angle == lbar_ang_end:
            left_bar_inc = bar_inc_init
    # Update right bar angle
    if rkey_pressed:
        body_rbar.angle = min(rbar_ang_end, body_rbar.angle + right_bar_inc)
        right_bar_inc += bar_inc_step
    else:
        body_rbar.angle = max(rbar_ang_start, body_rbar.angle - right_bar_inc)
        if body_rbar.angle == rbar_ang_end:
            right_bar_inc = bar_inc_init

def create_space():
    global screen, space, draw_options
    space = pymunk.Space()
    space.gravity = (0, 900)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    space.iterations = 50 # Esto mejora el número de iteraciones internas para resolver colisiones

def create_ball():
    global body_ball, space, ball_radius, center_x, center_y
    mass = 1.5
    moment = pymunk.moment_for_circle(mass, 0, ball_radius)
    body_ball = pymunk.Body(mass, moment)
    body_ball.position = center_x, center_y
    shape = pymunk.Circle(body_ball, ball_radius)
    shape.elasticity = 1.0
    shape.friction = 0.5
    shape.color = [0, 0, 255, 255]
    space.add(body_ball, shape)

def add_borders():
    global space, screen    
    WIDTH, HEIGHT = screen.get_size()
    static_lines = [
        pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), 5),           # left
        pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), 5),   # right
        #pymunk.Segment(space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 5),  # botton
        pymunk.Segment(space.static_body, (0, 0), (WIDTH, 0), 5)             # top
    ]
    for line in static_lines:
        line.elasticity = 0.8
        space.add(line)

def add_left_bar():
    global body_lbar, lbar_ang_start, space, screen
    body_lbar = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    posicion_pivote = 50, 0.73 * screen.get_height()
    body_lbar.position = posicion_pivote
    body_lbar.angle = lbar_ang_start
    a = (0, 0)
    b = (230, 0)
    segment = pymunk.Segment(body_lbar, a, b, 24)
    segment.elasticity = 1.0
    segment.friction = 0.5
    space.add(body_lbar, segment)

def add_right_bar():
    global body_rbar, rbar_ang_start, space, screen
    body_rbar = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    posicion_pivote = screen.get_width() - 50, 0.73 * screen.get_height()
    body_rbar.position = posicion_pivote
    body_rbar.angle = rbar_ang_start
    a = (230, 0)
    b = (0, 0)
    segment2 = pymunk.Segment(body_rbar, a, b, 24)
    segment2.elasticity = 1.0
    segment2.friction = 0.5
    space.add(body_rbar, segment2)

def main():
    global screen, running, game_over
    pygame.init()
    create_window()
    create_space()
    game_init()
    add_borders()
    add_left_bar()
    add_right_bar()
    clock = pygame.time.Clock()

    running = True
    while running:
        handle_events()
        update_bars()
        dt = 1 / 60
        for _ in range(10):
            space.step(dt / 10)
        screen.fill((0, 60, 0))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()