import pygame
pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders Screen")
player_size = 50
player_color = (255, 0, 0)
projectile_color = (0, 255, 0)

player_x = (width - player_size) // 2
player_y = height - player_size - 20

# Empty list for storing projectiles
projectiles = []

move_left = False
move_right = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Pressing keys
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            elif event.key == pygame.K_d:
                move_right = True
            elif event.key == pygame.K_RETURN:
                projectiles.append([player_x + player_size // 2, player_y])

        # Letting go of keys
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            elif event.key == pygame.K_d:
                move_right = False

    if move_left:
        player_x -= 0.25
    if move_right:
        player_x += 0.25

    # Constant y reduction for projectiles
    for projectile in projectiles:
        projectile[1] -= 1

    # Remove projectiles that go off screen by creating a new list
    projectiles = [projectile for projectile in projectiles if projectile[1] > 0]

    # Color the screen dark blue
    screen.fill((0, 0, 30))

    # Draw projectiles
    for projectile in projectiles:
        pygame.draw.rect(screen, projectile_color, (projectile[0], projectile[1], 5, 10))

    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))
    pygame.display.flip()

pygame.quit()
