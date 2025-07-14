import pygame
import math
LOGS_ALLOWED = True


# Global variables
screen = None
clock = None

# Ball parameters
ball_radius = 25
ball_angle = None
ball_step = None
center_x, center_y = 100, 100
ball_color = (100, 100, 100)
shadow_color = (180, 180, 180)
highlight_color = (255, 255, 255, 100)

# Logging function
def log(str):
    if LOGS_ALLOWED:
        print(str)

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
    log("Ball generated at center: ({}, {})".format(center_x, center_y))

# Function that update the ball posiiton
# center_x, center_y depending on a given angle and step
def update_ball_position(angle, step):
    global center_x, center_y, ball_angle, ball_step, ball_radius, screen
    # Si la bola toca un borde de la pantalla, invertir su dirección
    if center_x <= ball_radius or center_x >= screen.get_width() - ball_radius:
        # Invertir la dirección de la bola sentido horizontal
        ball_angle = (180 - ball_angle) % 360
        if center_x <= ball_radius:
            center_x = center_x + ball_radius//2
        else:
            center_x = center_x - ball_radius//2
    if center_y <= ball_radius or center_y >= screen.get_height() - ball_radius:
        # Invertir la dirección de la bola sentido vertical
        ball_angle = (-ball_angle) % 360        
        if center_y >= screen.get_height() - ball_radius: ball_step = 0
        else: center_y = center_y + ball_radius//2
    # Convert angle to radians
    angle_rad = -math.radians(angle)
    # Update position based on angle and step
    center_x += step * math.cos(angle_rad)
    center_y += step * math.sin(angle_rad)



# Init game variables
def game_init():
    global screen, ball_radius, center_x, center_y, ball_angle, ball_step
    # Initialize game variables
    center_x, center_y = screen.get_width() // 2, screen.get_height() // 2
    ball_radius = 25
    ball_angle = 35  # Initial angle in degrees
    ball_step = 5  # Step size for ball movement

# Create window
def create_window():
    global screen, clock
    screen = pygame.display.set_mode((800, 1000))
    pygame.display.set_caption("Mi primer juego")
    clock = pygame.time.Clock()

# Main game loop
def main():
    global screen, clock, ball_angle, ball_step
    
    # Init pygame and create an initial window
    pygame.init()
    create_window()
    game_init()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Analyze inputs and handle events

        # Aquí se actualiza la lógica del juego
        update_ball_position(ball_angle, ball_step)
       
        # Aquí se dibujan los objetos
        screen.fill((0, 0, 0))  # Limpiar pantalla (color negro)
        generate_ball()
        pygame.display.flip()  # Actualizar pantalla
        clock.tick(60)

    # Quit pygame
    pygame.quit()

# Execute the main loop
if __name__ == "__main__":
    main()