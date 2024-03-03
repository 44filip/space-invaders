import pygame

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders Screen")
player_size = 50
player_color = (255, 0, 0)
projectile_color = (0, 255, 0)
enemy_color = (0, 0, 255)
level = 1

player_x = (width - player_size) // 2
player_y = height - player_size - 20

# Empty list for storing projectiles
projectiles = []

move_left = False
move_right = False

# Enemy settings
enemy_size = 30
enemy_spacing = 40
enemies = []

total_enemy_width = 10 * (enemy_size + enemy_spacing) - enemy_spacing
start_x = (width - total_enemy_width) // 2

# Create a list to store the direction of each enemy
enemy_direction = 1

def spawn_enemies():
    for i in range(10):
        enemy_x = start_x + i * (enemy_size + enemy_spacing)
        enemy_y = 60
        enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size))

spawn_enemies()

clock = pygame.time.Clock()
fps = 60
player_speed = 10.0
projectile_speed = 20.0
enemy_speed = 4.0

# Score and level initialization
score = 0
font = pygame.font.Font(None, 36)

running = True
while running:
    clock.tick(fps)

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
                projectile_x = player_x + (player_size // 2) - 2
                projectiles.append([projectile_x, player_y])

        # Letting go of keys
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            elif event.key == pygame.K_d:
                move_right = False

    if move_left and player_x > 0:
        player_x -= player_speed
    if move_right and player_x < width - player_size:
        player_x += player_speed

    # Constant y reduction for projectiles
    for projectile in projectiles:
        projectile[1] -= projectile_speed

    # Update enemy positions based on their direction
    for enemy in enemies:
        enemy.x += enemy_speed * enemy_direction

    # Change direction and move down when reaching the screen edges
    if enemies and (enemies[-1].right >= width or enemies[0].left <= 0):
        enemy_direction *= -1
        for enemy in enemies:
            enemy.y += 10

    # Check for collisions between enemies and projectiles
    for enemy in enemies:
        for projectile in projectiles:
            if pygame.Rect(projectile[0], projectile[1], 5, 10).colliderect(enemy):
                projectiles.remove(projectile)
                enemies.remove(enemy)
                score += 1

    # Remove projectiles that go off screen by creating a new list
    projectiles = [projectile for projectile in projectiles if projectile[1] > 0]

    # Color the screen dark blue
    screen.fill((0, 0, 30))

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, enemy_color, enemy)

    # Draw projectiles
    for projectile in projectiles:
        pygame.draw.rect(screen, projectile_color, (projectile[0], projectile[1], 5, 10))

    # Draw player
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))

    # Draw score and level on the screen
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))

    # Get the rect of the text surface to determine its size
    score_rect = score_text.get_rect()
    level_rect = level_text.get_rect()

    # Set the position of the text based on the screen size and text size
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (width - level_rect.width - 10, 10))

    # Respawn enemies if all are killed
    if not enemies:
        level += 1
        enemy_speed += level // 5
        spawn_enemies()

    pygame.display.flip()

pygame.quit()
