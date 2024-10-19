import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 550
BIRD_WIDTH = 50
BIRD_HEIGHT = 35
PIPE_WIDTH = 70
PIPE_GAP = 150
GRAVITY = 0.25
BIRD_JUMP = -6
PIPE_SPEED = -3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load Bird Image
bird_img = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
bird_img.fill(BLUE)

# Bird Class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def draw(self):
        screen.blit(bird_img, (self.x, self.y))

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        if self.y + BIRD_HEIGHT > GROUND_HEIGHT:
            self.y = GROUND_HEIGHT - BIRD_HEIGHT
            self.velocity = 0

    def jump(self):
        self.velocity = BIRD_JUMP

# Pipe Class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, 400)
        self.top_pipe_height = self.height - PIPE_GAP

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.top_pipe_height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height, PIPE_WIDTH, SCREEN_HEIGHT - self.height))

    def update(self):
        self.x += PIPE_SPEED

# Game Loop
def game_loop():
    bird = Bird()
    pipes = []
    pipe_timer = 0
    score = 0
    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()
    game_over = False

    while True:
        screen.fill(WHITE)
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        if not game_over:
            bird.update()

            # Pipe Generation
            if pipe_timer > 100:
                pipes.append(Pipe())
                pipe_timer = 0

            # Update and Draw Pipes
            for pipe in pipes[:]:
                pipe.update()
                pipe.draw()
                if pipe.x + PIPE_WIDTH < 0:
                    pipes.remove(pipe)
                    score += 1

                # Check for collisions
                if bird.x + BIRD_WIDTH > pipe.x and bird.x < pipe.x + PIPE_WIDTH:
                    if bird.y < pipe.top_pipe_height or bird.y + BIRD_HEIGHT > pipe.height:
                        game_over = True

            pipe_timer += 1

        # Draw Bird
        bird.draw()

        # Ground
        pygame.draw.rect(screen, BLACK, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))

        # Draw Score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Check for Game Over
        if game_over:
            game_over_text = font.render("Game Over! Press R to Restart", True, BLACK)
            screen.blit(game_over_text, (50, SCREEN_HEIGHT // 2))
            pygame.display.update()

            # Restart Game
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    game_loop()

        pygame.display.update()
        clock.tick(60)

# Start Game
game_loop()
