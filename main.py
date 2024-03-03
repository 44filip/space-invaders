import pygame
import random
import sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders Screen")

player_color = (255, 0, 0)
projectile_color = (0, 255, 0)
enemy_color = (0, 0, 255)
star_color = (255, 255, 255)


player_size = 50
player_x = (width - player_size) // 2
player_y = height - player_size - 20
move_left = False
move_right = False

projectiles = []

level = 1

enemy_size = 30
enemy_spacing = 40
enemies = []
total_enemy_width = 10 * (enemy_size + enemy_spacing) - enemy_spacing
start_x = (width - total_enemy_width) // 2
enemy_direction = 1

def spawn_enemies():
    for row in range(3):
        for i in range(10):
            enemy_x = start_x + i * (enemy_size + enemy_spacing)
            enemy_y = 60 + row * (enemy_size + enemy_spacing)
            enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size))

spawn_enemies()

clock = pygame.time.Clock()
fps = 60
player_speed = 10.0
projectile_speed = 20.0
enemy_speed = 5.0

# Score and level initialization
score = 0
font = pygame.font.Font(None, 36)

# Main menu settings
menu_font = pygame.font.Font(None, 48)
menu_text_color = (255, 255, 255)
menu_options = ["Start Game", "Exit"]
selected_option = None

def draw_main_menu():
    screen.fill((0, 0, 30))
    for i, option in enumerate(menu_options):
        text = menu_font.render(option, True, menu_text_color)
        text_rect = text.get_rect(center=(width // 2, height // 2 - 50 + i * 70))
        screen.blit(text, text_rect)

# Main menu loop
in_main_menu = True
while in_main_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_main_menu = False
            pygame.quit()
            sys.exit()

    # Check for mouse clicks
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]

    for i, option in enumerate(menu_options):
        text_rect = menu_font.render(option, True, menu_text_color).get_rect(center=(width // 2, height // 2 - 50 + i * 70))
        if text_rect.collidepoint(mouse_x, mouse_y) and mouse_clicked:
            selected_option = i
            if selected_option == 0:
                in_main_menu = False
            elif selected_option == 1:
                pygame.quit()
                sys.exit()

    draw_main_menu()
    pygame.display.flip()

# Function to display the game over screen
def game_over_screen(final_score):
    screen.fill((0, 0, 30))
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
    final_score_text = font.render(f"Your score: {final_score}", True, (255, 255, 255))

    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 50))
    screen.blit(final_score_text, (width // 2 - final_score_text.get_width() // 2, height // 2 + 50))
    pygame.display.flip()

# Game loop
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
    leftmost_enemy = min(enemies, key=lambda enemy: enemy.x)
    rightmost_enemy = max(enemies, key=lambda enemy: enemy.x + enemy_size)

    if enemies and (rightmost_enemy.right >= width or leftmost_enemy.left <= 0):
        enemy_direction *= -1
        for enemy in enemies:
            enemy.y += height * 0.02
            enemy.x += enemy_speed * enemy_direction

    # Check for collisions between enemies and projectiles
    for enemy in enemies:
        for projectile in projectiles:
            if pygame.Rect(projectile[0], projectile[1], 5, 10).colliderect(enemy):
                projectiles.remove(projectile)
                enemies.remove(enemy)
                score += 1
                
    # Check for collisions between player and enemies
    for enemy in enemies:
        if pygame.Rect(player_x, player_y, player_size, player_size).colliderect(enemy):
            game_over_screen(score)
            pygame.time.delay(3000)  # Pause for 3 seconds to show the game over screen
            running = False
            break

    # Check if enemies leave the bottom part of the screen
    for enemy in enemies.copy():
        if enemy.bottom > height:
            game_over_screen(score)
            pygame.time.delay(3000)
            running = False
            break

    # Remove projectiles that go off screen by creating a new list
    projectiles = [projectile for projectile in projectiles if projectile[1] > 0]

    # Color the screen dark blue
    screen.fill((0, 0, 30))

    # Draw stars
    for _ in range(5):
        star_x = random.randint(0, width)
        star_y = random.randint(0, height)
        pygame.draw.circle(screen, star_color, (star_x, star_y), 1)

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
        enemy_speed += 0.25
        spawn_enemies()

    pygame.display.flip()

pygame.quit()