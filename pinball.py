import pygame
pygame.init()


# Create window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mi primer juego")

# Main game loop
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Aquí se actualiza la lógica del juego
        screen.fill((0, 0, 0))  # Limpiar pantalla (color negro)

        # Aquí se dibujan los objetos
        pygame.display.flip()  # Actualizar pantalla

    # Quit pygame
    pygame.quit()

# Execute the main loop
if __name__ == main:
    main()
