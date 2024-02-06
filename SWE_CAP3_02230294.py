import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 600
HEIGHT = 400
FPS = 60

# Load your own background image
background_image = pygame.image.load(r'C:\Users\DELL\Desktop\CSF\Practical Codes\cap3\wallpaper designs for walls living room modern.jpg')

# Player settings
player_size = 40  # Decreased size
player_speed = 5

# Load your own player image
player_image = pygame.image.load(r'C:\Users\DELL\Desktop\CSF\Practical Codes\cap3\rspaceship.png')
player_image = pygame.transform.scale(player_image, (player_size, player_size))

# Custom object settings
object_size = 40  # Decreased size
object_speed = 3
object_speed_increase_interval = 15  # in seconds
object_speed_increase_amount = 2

# Load your own falling object image
object_image = pygame.image.load(r'C:\Users\DELL\Desktop\CSF\Practical Codes\cap3\metoer.jpg')
object_image = pygame.transform.scale(object_image, (object_size, object_size))

# Start button settings
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
start_text = "Start Game"

# Restart button settings
restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
restart_text = "Restart Game"

# Sound settings
game_over_sound = pygame.mixer.Sound(r'C:\Users\DELL\Desktop\CSF\Practical Codes\cap3\game-over-arcade-6435.mp3')  # Replace 'game_over_sound.wav' with the path to your sound file

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodger Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Player
player_rect = player_image.get_rect(center=(WIDTH // 2, HEIGHT - player_size - 10))

# Custom objects
custom_objects = []

# Font for the menu text
font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Function to create a button
def draw_button(rect, color, text):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, DARK_GRAY, rect, 3)

    button_text = font.render(text, True, WHITE)
    text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect.topleft)

# Function to generate a new custom object
def spawn_custom_object():
    x = random.randint(0, WIDTH - object_size)
    y = -object_size
    new_object = pygame.Rect(x, y, object_size, object_size)
    custom_objects.append(new_object)

# Function to display the menu
def show_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
                return True  # Start the game if the start button is clicked

        screen.blit(background_image, (0, 0))
        
        draw_button(start_button, GRAY, start_text)

        pygame.display.flip()
        clock.tick(FPS)

# Show the menu initially
show_menu()

# Timer variables
start_time = pygame.time.get_ticks()
current_time = 0

# Main game loop
running = True
game_started = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_started:
        # Wait for the player to press the start button
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
                game_started = True
        continue  # Skip the rest of the loop until the game starts

    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed

    # Calculate elapsed time
    current_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert to seconds

    # Spawn new custom object with a certain probability
    if random.random() < 0.02:
        spawn_custom_object()

    # Increase object speed every 30 seconds
    if current_time >= object_speed_increase_interval:
        object_speed += object_speed_increase_amount
        start_time = pygame.time.get_ticks()

    # Move custom objects
    for obj in custom_objects:
        obj.y += object_speed
        if obj.colliderect(player_rect):
            # Game Over
            game_over_sound.play()  # Play the game over sound
            game_started = False
            while not show_menu():  # Wait for the player to press the restart button
                pass
            # Reset variables for a new game
            custom_objects = []
            object_speed = 3
            start_time = pygame.time.get_ticks()

    # Remove off-screen custom objects
    custom_objects = [obj for obj in custom_objects if obj.y < HEIGHT]

    # Draw background
    screen.blit(background_image, (0, 0))

    # Draw player
    screen.blit(player_image, player_rect.topleft)

    # Draw custom objects
    for obj in custom_objects:
        screen.blit(object_image, obj.topleft)

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()



