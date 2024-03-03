# Screen dimensions
width, height = 800, 600

# Pygame clock FPS
fps = 60

# Starting score
score = 0

# Starting level
level = 1

# Player variables
player_size = 50
player_speed = 10.0
player_x = (width - player_size) // 2
player_y = height - player_size - 20

# Projectile variables
projectile_speed = 20.0

# Enemy variables
enemy_size = 30
enemy_speed = 2.5
enemy_spacing = 40
total_enemy_width = 10 * (enemy_size + enemy_spacing) - enemy_spacing
start_x = (width - total_enemy_width) // 2
enemy_direction = 1

# Star color
star_color = (255, 255, 255)



