import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAVITY = 0.5
BOUNCE_FACTOR = 0.7
FONT_SIZE = 30
FINEPRINT_SIZE = 20
LEVEL_UP_SCORE = 13

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bounce!")

# Font for displaying score and level
font = pygame.font.SysFont(None, FONT_SIZE)
fineprint_font = pygame.font.SysFont(None, FINEPRINT_SIZE)

# Ball properties
ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 3
ball_speed_y = 3

# Define number of obstacles for each level
num_obstacles_per_level = [3, 4, 5]

# Game variables
score = 0
level = 1
game_over = False

clock = pygame.time.Clock()

def ball_collides_with_obstacle(ball_x, ball_y, ball_radius, obstacle):
    ox, oy, ow, oh = obstacle
    closest_x = max(ox, min(ball_x, ox + ow))
    closest_y = max(oy, min(ball_y, oy + oh))
    distance_x = ball_x - closest_x
    distance_y = ball_y - closest_y
    return (distance_x ** 2 + distance_y ** 2) < (ball_radius ** 2)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def generate_random_obstacles(num_obstacles):
    obstacles = []
    for _ in range(num_obstacles):
        x = random.randint(50, WIDTH - 150)
        y = random.randint(50, HEIGHT - 150)
        w = random.randint(50, 150)
        h = random.randint(20, 50)
        obstacles.append((x, y, w, h))
    return obstacles

def reset_game():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, score, level, game_over, obstacles
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed_x = 3
    ball_speed_y = 3
    score = 0
    level = 1
    game_over = False
    obstacles = generate_random_obstacles(num_obstacles_per_level[level - 1])

def advance_level():
    global level, ball_x, ball_y, ball_speed_x, ball_speed_y, obstacles
    level += 1
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed_x = 3
    ball_speed_y = 3
    obstacles = generate_random_obstacles(num_obstacles_per_level[level - 1])

# Initialize the first set of obstacles
obstacles = generate_random_obstacles(num_obstacles_per_level[level - 1])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                reset_game()
            else:
                mouse_x, mouse_y = event.pos
                ball_speed_x = (mouse_x - ball_x) / 10
                ball_speed_y = (mouse_y - ball_y) / 10

    if not game_over:
        # Update ball position
        ball_speed_y += GRAVITY
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Handle bouncing off the edges
        if ball_x - ball_radius < 0 or ball_x + ball_radius > WIDTH:
            ball_speed_x = -ball_speed_x * BOUNCE_FACTOR
            if ball_x - ball_radius < 0:
                ball_x = ball_radius
            else:
                ball_x = WIDTH - ball_radius

        if ball_y - ball_radius < 0 or ball_y + ball_radius > HEIGHT:
            ball_speed_y = -ball_speed_y * BOUNCE_FACTOR
            if ball_y - ball_radius < 0:
                ball_y = ball_radius
            else:
                ball_y = HEIGHT - ball_radius

        # Handle bouncing off obstacles
        for obstacle in obstacles:
            if ball_collides_with_obstacle(ball_x, ball_y, ball_radius, obstacle):
                ox, oy, ow, oh = obstacle
                if ball_x > ox and ball_x < ox + ow:
                    ball_speed_y = -ball_speed_y * BOUNCE_FACTOR
                    if ball_y < oy:
                        ball_y = oy - ball_radius
                    else:
                        ball_y = oy + oh + ball_radius
                if ball_y > oy and ball_y < oy + oh:
                    ball_speed_x = -ball_speed_x * BOUNCE_FACTOR
                    if ball_x < ox:
                        ball_x = ox - ball_radius
                    else:
                        ball_x = ox + ow + ball_radius

                # Increment score for bouncing off an obstacle
                score += 1

                # Check for level up
                if score >= level * LEVEL_UP_SCORE:
                    if level < len(num_obstacles_per_level):
                        advance_level()

        # Game over condition
        if ball_y + ball_radius >= HEIGHT:
            game_over = True

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius)
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    # Display score and level
    draw_text(f"Score: {score}", font, WHITE, screen, 10, 10)
    draw_text(f"Level: {level}", font, WHITE, screen, 10, 40)

    if game_over:
        draw_text("Game Over! Click to Restart", font, WHITE, screen, WIDTH // 4, HEIGHT // 2)

    # Display fine print
    draw_text("Created by Isaac Tomeho", fineprint_font, WHITE, screen, WIDTH - 220, HEIGHT - 30)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
