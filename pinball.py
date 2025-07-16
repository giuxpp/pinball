import pygame
import pymunk
import pymunk.pygame_util
import math

LOGS_ALLOWED = True

# Global variables
SCREEN_WIDTH = 800
running = True 
game_over = True
bar_colission = False
rkey_pressed, lkey_pressed = False, False
screen = None
space = None
draw_options = None
left_bar, right_bar = None, None

# Ball parameters
ball_radius = None
ball_angle = None
ball_step = None
ball_step_init = 10
center_x, center_y = 100, 100
ball_color = (100, 100, 100)
shadow_color = (180, 180, 180)
highlight_color = (255, 255, 255, 100)

# Bar parameters (generic)
bar_length = None  # Will be set in game_init
bar_width = 30
bar_color = (200, 200, 102)  # Mustard yellow color
bar_y_offset = None
left_bar_inc = None
right_bar_inc = None
bar_inc_init = 2.5   # Defines how "responsive" the bars are when pressed
bar_inc_step = 0.6  # Increment step for bar angle when pressed
bar_colission_ctr_init = 8
bar_colission_ctr = None

# Left Bar parameters
left_bar_angle_initial = -45
left_bar_angle = None

# Right Bar parameters
right_bar_angle_initial = 135
right_bar_angle = None

# Logging function
def log(str): 
    if LOGS_ALLOWED: print(str)


# Init game variables
def game_init():
    global screen, ball_radius, center_x, center_y, ball_angle, ball_step, bar_length, left_bar_angle, left_bar_angle_initial
    global bar_length, right_bar_angle, right_bar_angle_initial, bar_width, bar_y_offset, game_over
    global bar_colission_ctr, bar_colission_ctr_init, left_bar_inc, right_bar_inc, bar_inc_init
    global ball_step_init

    # Set ball parameters
    center_x, center_y = screen.get_width() // 2, screen.get_height() // 2
    ball_radius = screen.get_height() // 30  # Make radius of ball depend on screen size
    ball_angle = 75  # Initial angle in degrees
    ball_step = ball_step_init  # Step size for ball movement    
    # Set bar parameters
    bar_length = screen.get_width() // 2.85
    bar_colission_ctr = bar_colission_ctr_init
    left_bar_inc = bar_inc_init
    right_bar_inc = bar_inc_init
    # Set bar y offset depending on screen height
    bar_y_offset = 250 #screen.get_height() // 4
    left_bar_angle = left_bar_angle_initial
    right_bar_angle = right_bar_angle_initial
    # Set game state
    game_over = False
    # Create the ball at the start of the game
    create_ball()

# Create window
def create_window():
    global screen, SCREEN_WIDTH
    screen_height = SCREEN_WIDTH * 1.5
    screen = pygame.display.set_mode((SCREEN_WIDTH, screen_height))
    pygame.display.set_caption("-- Pinball game --")

# Handle events and user inputs from keyboard
def handle_events():
    global running, left_bar_angle, right_bar_angle
    global lkey_pressed, rkey_pressed, game_over
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        # Handle key press           
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_LEFT:
                lkey_pressed = True
                log("Left key pressed")
            if ev.key == pygame.K_RIGHT:
                rkey_pressed = True
                log("Right key pressed")
            if ev.key == pygame.K_RETURN and game_over:
                # Reset game state
                game_init()
                log("Game reset")
            if ev.key == pygame.K_ESCAPE:
                if game_over:
                    log("Game over, press ENTER to reset")
                    running = False
                else:
                    game_over = True
                    log("Game paused, press ENTER to reset")
        # Handle key release
        if ev.type == pygame.KEYUP:
            if ev.key == pygame.K_LEFT:
                lkey_pressed = False
                log("Left key released")
            if ev.key == pygame.K_RIGHT:
                rkey_pressed = False
                log("Right key released")

def update_bars():
    global left_bar_angle, left_bar_angle_initial, right_bar_angle, right_bar_angle_initial
    global lkey_pressed, rkey_pressed, left_bar_inc, right_bar_inc, bar_colission, bar_inc_init
    global bar_inc_step # Increment step for bar angle when pressed
    global body_lbar
    # Update left bar angle depending on whether the left key is keep pressed
    if lkey_pressed:                        
            body_lbar.angle  = min(0, body_lbar.angle + left_bar_inc)  # Keep it at or above initial angle
            left_bar_inc += bar_inc_step
    else:
        left_bar_angle = max(left_bar_angle_initial, left_bar_angle- left_bar_inc)  # Reset to initial angle if not pressed
        if left_bar_angle == left_bar_angle_initial:
            left_bar_inc = bar_inc_init
    # Update right bar angle depending on whether the right key is keep pressed
    if rkey_pressed:
        if not bar_colission:
            right_bar_angle = min(180, right_bar_angle + right_bar_inc)  # Keep it at or below initial angle
            right_bar_inc += bar_inc_step
    else:
        right_bar_angle = max(right_bar_angle_initial, right_bar_angle - right_bar_inc)
        if right_bar_angle == right_bar_angle_initial:
            right_bar_inc = bar_inc_init
    if bar_colission:
        # If a bar collision has been detected, we reset the bar collision flag after a few frames
        global bar_colission_ctr, bar_colission_ctr_init
        bar_colission_ctr -= 1
        if bar_colission_ctr <= 0:
            bar_colission = False
            bar_colission_ctr = bar_colission_ctr_init

def create_space():
    global screen, space, draw_options
    # Espacio pymunk con gravedad
    space = pymunk.Space()
    space.gravity = (0, 900)
    # Dibujador de pymunk en pygame
    draw_options = pymunk.pygame_util.DrawOptions(screen)

# Crear bola con física
body_ball = None
def create_ball():
    mass = 1
    moment = pymunk.moment_for_circle(mass, 0, ball_radius)
    body_ball = pymunk.Body(mass, moment)
    body_ball.position =center_x, center_y
    shape = pymunk.Circle(body_ball, ball_radius)
    shape.elasticity = 0.9
    shape.friction = 0.5
    shape.color = [0, 0, 255, 255]
    space.add(body_ball, shape)

def add_borders():
    # Add static lines to the space to create borders
    global space, screen    
    WIDTH, HEIGHT = screen.get_size()
    # Create static lines for Left, right, and bottom borders
    static_lines = [
        pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), 5),         # izquierda
        pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), 5), # derecha
        pymunk.Segment(space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 5) # piso
    ]
    for line in static_lines:
        line.elasticity = 0.8
        space.add(line)

body_lbar = None
def add_left_bar():
    # Add left bar to the space
    global space, screen, bar_length, bar_width, bar_y_offset, left_bar_angle
    global left_bar, right_bar, body_lbar
    x0 = 0
    y0 = screen.get_height() - bar_y_offset
    angle_rad = math.radians(left_bar_angle)
    x1 = x0 + bar_length * math.cos(angle_rad)
    y1 = y0 - bar_length * math.sin(angle_rad)

    body_lbar = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    # The bar's endpoints are in world coordinates, so use them directly
    a = (x0, y0)
    b = (x1, y1)
    left_bar = pymunk.Segment(body_lbar, a, b, bar_width // 2)
    left_bar.elasticity = 0.8
    space.add(body_lbar, left_bar)

# Main game loop
def main():
    global screen, running, game_over
    
    # Init pygame and create an initial window
    pygame.init()    # init step 1    
    create_window()  # init step 2
    create_space()   # init step 3
    game_init()      # init step 4    
    add_borders()    # Add borders to the game space     
    add_left_bar()
    clock = pygame.time.Clock()

    running = True
    while running:
        # Analyze inputs and handle events
        handle_events()
        
        # Aquí se actualiza la lógica del juego
        update_bars()
        #if not game_over:
            #update_ball_position(ball_angle, ball_step)
            #check_bar_collisions()    
        
        # Actualización de física
        space.step(1/60)

        # Draw the objects and update the screen
        screen.fill((0, 60, 0))  # Clear screen (dark green)
        space.debug_draw(draw_options)
        #generate_ball()        
        #draw_left_bar()
        #draw_right_bar()

        pygame.display.flip()    # Update the display
        clock.tick(60)           # Limit to 60 FPS

    # Quit pygame
    pygame.quit()

# Execute the main loop
if __name__ == "__main__":
    main()