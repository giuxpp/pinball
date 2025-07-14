import pygame
import math
LOGS_ALLOWED = True


# Global variables
screen = None

# Ball parameters
ball_radius = 25
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
    global center_x, center_y
    # Convert angle to radians
    angle_rad = -math.radians(angle)
    # Update position based on angle and step
    center_x += step * math.cos(angle_rad)
    center_y += step * math.sin(angle_rad)

# Init game variables
def game_init():
    global screen, ball_radius, center_x, center_y, ball_color, shadow_color, highlight_color
    # Initialize game variables
    center_x, center_y = screen.get_width() // 2, screen.get_height() // 2

# Create window
def create_window():
    global screen
    screen = pygame.display.set_mode((800, 1000))
    pygame.display.set_caption("Mi primer juego")

# Main game loop
def main():
    global screen
    
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
        update_ball_position(110, 1)
       
        # Aquí se dibujan los objetos
        screen.fill((0, 0, 0))  # Limpiar pantalla (color negro)
        generate_ball()
        pygame.display.flip()  # Actualizar pantalla

    # Quit pygame
    pygame.quit()

# Execute the main loop
if __name__ == "__main__":
    main()