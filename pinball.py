import pygame
import math

LOGS_ALLOWED = True

# Global variables
screen = None
SCREEN_WIDTH = 800
running = True 
game_over = True
bar_colission = False
rkey_pressed, lkey_pressed = False, False

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

# Creates a "ball" at the center of the window
def generate_ball():
    global screen, ball_radius, ball_color, shadow_color, highlight_color, center_x, center_y 
    # Draw shadow
    shadow_offset = 8
    pygame.draw.circle(screen, shadow_color, (center_x + shadow_offset, center_y + shadow_offset), ball_radius)
    # Draw main ball
    pygame.draw.circle(screen, ball_color, (center_x, center_y), ball_radius)
    # Draw highlight (simulate light reflection)
    highlight_surface = pygame.Surface((ball_radius*2, ball_radius*2), pygame.SRCALPHA)
    pygame.draw.ellipse(highlight_surface, highlight_color, (ball_radius//2, ball_radius//2, ball_radius, ball_radius//2))
    screen.blit(highlight_surface, (center_x - ball_radius, center_y - ball_radius))

# Function that update the ball posiiton center_x, center_y depending on a given angle and step
def update_ball_position(angle, step):
    global center_x, center_y, ball_angle, ball_step, ball_radius, screen, game_over
    # Check if the ball touches the screen borders
    if center_x <= ball_radius or center_x >= screen.get_width() - ball_radius:
        # Invert the direction of the ball horizontally
        ball_angle = (180 - ball_angle) % 360
        if center_x <= ball_radius:
            center_x = center_x + ball_radius//2
        else:
            center_x = center_x - ball_radius//2
    if center_y <= ball_radius or center_y >= screen.get_height() - ball_radius:
        # Invert the direction of the ball vertically
        ball_angle = (-ball_angle) % 360        
        if center_y >= screen.get_height() - ball_radius: 
            ball_step = 0
            game_over = True
        else: 
            center_y = center_y + ball_radius//2
    # Convert angle to radians
    angle_rad = -math.radians(angle)
    # Update position based on angle and step
    center_x += step * math.cos(angle_rad)
    center_y += step * math.sin(angle_rad)

# Draws a bar at the bottom left, with a given angle (degrees)
def draw_left_bar():
    global screen, left_bar_angle, bar_length, bar_width, bar_color, bar_y_offset
    x0 = 0
    y0 = screen.get_height() - bar_y_offset
    angle_rad = math.radians(left_bar_angle)
    x1 = x0 + bar_length * math.cos(angle_rad)
    y1 = y0 - bar_length * math.sin(angle_rad)
    pygame.draw.line(screen, bar_color, (x0, y0), (x1, y1), bar_width)
    # Draw circles at both ends for rounded edges
    pygame.draw.circle(screen, bar_color, (int(x1), int(y1)), bar_width // 2)

# Draws a bar at the bottom right, vertically symmetric to the left bar
def draw_right_bar():
    global screen, right_bar_angle, bar_length, bar_width, bar_color, bar_y_offset
    x0 = screen.get_width()
    y0 = screen.get_height() - bar_y_offset
    # Mirror horizontally: angle is measured from the right
    angle_rad = math.radians(180 - right_bar_angle)
    x1 = x0 + bar_length * -math.cos(angle_rad)
    y1 = y0 - bar_length * -math.sin(angle_rad)
    pygame.draw.line(screen, bar_color, (x0, y0), (x1, y1), bar_width)
    # Draw circles at both ends for rounded edges
    pygame.draw.circle(screen, bar_color, (int(x1), int(y1)), bar_width // 2)

# Collision detection between ball and bars
def check_bar_collisions():
    global center_x, center_y, ball_radius, bar_length, bar_width, left_bar_angle, right_bar_angle, bar_y_offset, screen, ball_angle

    def get_bar_endpoints(x0, y0, angle_deg, length):
        # This function calculates the endpoints of a bar given its starting point, angle, and length
        angle_rad = math.radians(angle_deg)
        x1 = x0 + length * math.cos(angle_rad)
        y1 = y0 - length * math.sin(angle_rad)
        return (x0, y0), (x1, y1)

    def ball_bar_collision(bar_p1, bar_p2, bar_width):
        # Vector from bar_p1 to bar_p2
        bx, by = bar_p1
        ex, ey = bar_p2
        dx, dy = ex - bx, ey - by
        # Vector from bar_p1 to ball center
        fx, fy = center_x - bx, center_y - by
        # Project point onto bar segment
        length_sq = dx*dx + dy*dy
        if length_sq == 0:
            return False
        t = (fx * dx + fy * dy) / length_sq
        t = max(0, min(1, t))
        closest_x = bx + t * dx
        closest_y = by + t * dy
        dist = math.hypot(center_x - closest_x, center_y - closest_y)
        return dist <= ball_radius + bar_width//2

    # Function to check if the ball is moving on right or left direction dependin on the angle
    def get_ball_direction():
        # Returns True if the ball is moving to the right, False if to the left
        if 0 <= ball_angle < 180:
            return "right"
        else:
            return "left"

    # Left bar
    left_x0 = 0
    left_y0 = screen.get_height() - bar_y_offset
    left_p1, left_p2 = get_bar_endpoints(left_x0, left_y0, left_bar_angle, bar_length)
    # Right bar
    right_x0 = screen.get_width()
    right_y0 = screen.get_height() - bar_y_offset
    right_p1, right_p2 = get_bar_endpoints(right_x0, right_y0, -right_bar_angle, bar_length)
    # Bar collisions
    if ball_bar_collision(left_p1, left_p2, bar_width) or ball_bar_collision(right_p1, right_p2, bar_width):
        ball_angle = (-ball_angle) % 360
        center_y -= ball_radius // 2
        log("Ball collided with bar")
        global bar_colission
        bar_colission = True
        # In order to avoid the ball sticking to the bar, we adjust the position
        # depending on the direction of the ball
        if get_ball_direction() == "right":
            center_x -= ball_radius // 2
        else:
            center_x += ball_radius


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
    # Update left bar angle depending on whether the left key is keep pressed
    if lkey_pressed:                
        if not bar_colission:
            left_bar_angle = min(0, left_bar_angle + left_bar_inc)  # Keep it at or above initial angle
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

# Main game loop
def main():
    global screen, running, game_over
    
    # Init pygame and create an initial window
    pygame.init()
    clock = pygame.time.Clock()
    create_window()
    game_init()
    
    running = True
    while running:
        # Analyze inputs and handle events
        handle_events()
        
        # Aquí se actualiza la lógica del juego
        update_bars()
        if not game_over:
            update_ball_position(ball_angle, ball_step)
            check_bar_collisions()    
        
        # Draw the objects and update the screen
        screen.fill((0, 60, 0))  # Clear screen (dark green)
        generate_ball()
        draw_left_bar()
        draw_right_bar()
        pygame.display.flip()    # Update the display
        clock.tick(60)           # Limit to 60 FPS

    # Quit pygame
    pygame.quit()

# Execute the main loop
if __name__ == "__main__":
    main()