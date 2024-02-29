import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
FONT_NAME = pygame.font.match_font("arial")

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Dash")
clock = pygame.time.Clock()

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT // 2
        self.velocity = 0
        self.gravity = 1

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

        # Check collision with platforms
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = -15  # Adjust jump strength as needed

# Platform Class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Power-up Class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 3  # Adjust power-up speed as needed

# Game Variables
score = 0
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(10):
    platform = Platform(random.randint(0, WIDTH - 100), random.randint(100, HEIGHT - 100))
    all_sprites.add(platform)
    platforms.add(platform)

# Game Fonts
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Game Loop
running = True
while running:
    # Process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # Update
    all_sprites.update()

    # Check collision between player and platforms
    if pygame.sprite.spritecollide(player, platforms, False):
        player.velocity = 0

    # Check collision between player and power-ups
    power_up_collisions = pygame.sprite.spritecollide(player, power_ups, True)
    for power_up in power_up_collisions:
        # Apply power-up effects
        score += 10  # Example: Increase score by 10 for each power-up collected

    # Generate new platforms
    while len(platforms) < 10:
        platform = Platform(random.randint(0, WIDTH - 100), random.randint(-50, -20))
        all_sprites.add(platform)
        platforms.add(platform)

    # Draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    draw_text(screen, "Score: " + str(score), 24, WIDTH // 2, 10)

    # Flip the display
    pygame.display.flip()
    clock.tick(FPS)

# Quit the game
pygame.quit()
