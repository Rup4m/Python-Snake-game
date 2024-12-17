import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game with Big Snakes and Score")

# Colors (Darker tone version)
green = (0, 255, 0)  # Snake body color
dark_green = (0, 200, 0)  # Snake head color
red = (255, 0, 0)    # Food color
black = (0, 0, 0)    # Background color
white = (255, 255, 255)  # Text color
purple = (55, 0, 120)    # Darker gradient color 1
blue = (0, 0, 100)       # Darker gradient color 2

# Snake settings
snake_size = 20
snake_speed = 10

# Font for text
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Clock
clock = pygame.time.Clock()

# Function to draw gradient background with smooth transition
def draw_gradient_background(screen, color1, color2):
    for i in range(height):
        r = color1[0] + (color2[0] - color1[0]) * i // height
        g = color1[1] + (color2[1] - color1[1]) * i // height
        b = color1[2] + (color2[2] - color1[2]) * i // height
        pygame.draw.line(screen, (r, g, b), (0, i), (width, i))

# Function to display score
def display_score(score):
    value = score_font.render(f"Score: {score}", True, white)
    screen.blit(value, [0, 0])

# Function to display the number of lives
def display_lives(lives):
    lives_text = font_style.render(f"Lives: {lives}", True, white)
    screen.blit(lives_text, [width - 120, 0])

# Function to display messages
def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3 + y_offset])

# Function to generate a big snake (enemy) that hunts the player
def generate_big_snake():
    snake_body = []
    head_x = random.randint(0, width - snake_size)
    head_y = random.randint(0, height - snake_size)
    for i in range(5):  # Make a big snake with 5 segments
        snake_body.append([head_x, head_y + i * snake_size])  # Create a big snake vertically
    return snake_body

# Game loop
def game_loop():
    lives = 3
    score = 0
    x = width // 2
    y = height // 2
    x_change = 0
    y_change = 0

    snake_list = []
    snake_length = 1

    # Food position
    food_x = random.randint(0, (width - snake_size) // snake_size) * snake_size
    food_y = random.randint(0, (height - snake_size) // snake_size) * snake_size

    running = True
    game_over = False

    # Store the time the game started
    start_ticks = pygame.time.get_ticks()

    # Big snake settings
    big_snake = []
    big_snake_hunting_time = 0
    big_snake_time = 0  # Time when the big snake should appear

    # Initial gradient colors (darker tones)
    gradient_color1 = purple
    gradient_color2 = blue

    while running:
        while game_over:
            screen.fill(black)
            message("Game Over! Press C to Play Again or Q to Quit", white)
            display_score(score)
            display_lives(lives)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        game_loop()  # Restart the game
                    if event.key == pygame.K_q:
                        running = False
                        game_over = False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -1
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = 1
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -1
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = 1
                    x_change = 0

        # Update snake position smoothly
        x += x_change * snake_speed
        y += y_change * snake_speed

        # Check if the snake hits the walls
        if x < 0 or x >= width or y < 0 or y >= height:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                # Reset snake and food
                x = width // 2
                y = height // 2
                x_change = 0
                y_change = 0
                snake_list = []
                snake_length = 1
                food_x = random.randint(0, (width - snake_size) // snake_size) * snake_size
                food_y = random.randint(0, (height - snake_size) // snake_size) * snake_size

        # Check for big snake every 15 seconds
        time_elapsed = (pygame.time.get_ticks() - start_ticks) / 1000  # Convert to seconds
        if time_elapsed >= big_snake_time + 15:
            big_snake_time = time_elapsed
            big_snake = generate_big_snake()  # Spawn a big snake
            big_snake_hunting_time = time_elapsed + 5  # Big snake will hunt for 5 seconds

        # If the big snake is hunting
        if time_elapsed >= big_snake_time and time_elapsed <= big_snake_hunting_time:
            # Move big snake towards player position
            for i in range(5):
                if big_snake[i][0] < x:
                    big_snake[i][0] += 1
                elif big_snake[i][0] > x:
                    big_snake[i][0] -= 1

                if big_snake[i][1] < y:
                    big_snake[i][1] += 1
                elif big_snake[i][1] > y:
                    big_snake[i][1] -= 1

            # Check if the player's snake collides with the big snake
            for segment in big_snake:
                if segment == [x, y]:
                    game_over = True

            # Draw big snake
            for segment in big_snake:
                pygame.draw.rect(screen, red, pygame.Rect(segment[0], segment[1], snake_size, snake_size))

        # Change the background gradient color every 20 seconds
        if time_elapsed >= 20:
            gradient_color1 = (random.randint(0, 100), random.randint(0, 100), random.randint(50, 150))  # Darker tone
            gradient_color2 = (random.randint(0, 100), random.randint(0, 100), random.randint(50, 150))  # Darker tone
            start_ticks = pygame.time.get_ticks()  # Reset the timer

        # Smooth transition of colors
        transition_time = 5  # seconds for smooth transition
        transition_progress = (pygame.time.get_ticks() - start_ticks) / (transition_time * 1000)

        if transition_progress < 1:
            smooth_color1 = (
                int(gradient_color1[0] * transition_progress + gradient_color1[0] * (1 - transition_progress)),
                int(gradient_color1[1] * transition_progress + gradient_color1[1] * (1 - transition_progress)),
                int(gradient_color1[2] * transition_progress + gradient_color1[2] * (1 - transition_progress)),
            )
            smooth_color2 = (
                int(gradient_color2[0] * transition_progress + gradient_color2[0] * (1 - transition_progress)),
                int(gradient_color2[1] * transition_progress + gradient_color2[1] * (1 - transition_progress)),
                int(gradient_color2[2] * transition_progress + gradient_color2[2] * (1 - transition_progress)),
            )
        else:
            smooth_color1 = gradient_color1
            smooth_color2 = gradient_color2

        # Draw gradient background
        draw_gradient_background(screen, smooth_color1, smooth_color2)

        # Draw food
        pygame.draw.circle(screen, red, (food_x + snake_size // 2, food_y + snake_size // 2), snake_size // 2)

        # Update snake
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check collision with self
        for segment in snake_list[:-1]:
            if segment == snake_head:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    # Reset snake and food
                    x = width // 2
                    y = height // 2
                    x_change = 0
                    y_change = 0
                    snake_list = []
                    snake_length = 1
                    food_x = random.randint(0, (width - snake_size) // snake_size) * snake_size
                    food_y = random.randint(0, (height - snake_size) // snake_size) * snake_size

        # Draw the snake
        for segment in snake_list[:-1]:
            pygame.draw.circle(screen, green, (segment[0] + snake_size // 2, segment[1] + snake_size // 2), snake_size // 2)

        # Draw the snake head (different color)
        pygame.draw.circle(screen, dark_green, (snake_list[-1][0] + snake_size // 2, snake_list[-1][1] + snake_size // 2), snake_size // 2)

        # Check if snake eats food
        if x == food_x and y == food_y:
            # Respawn food
            food_x = random.randint(0, (width - snake_size) // snake_size) * snake_size
            food_y = random.randint(0, (height - snake_size) // snake_size) * snake_size
            snake_length += 1
            score += 10

        # Display score and lives
        display_score(score)
        display_lives(lives)

        # Update the display
        pygame.display.update()

        # Set the speed of the snake
        clock.tick(15)

    pygame.quit()

# Start the game
game_loop()
