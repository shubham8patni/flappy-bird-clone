import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1800  # milliseconds
GROUND_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
SKY_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Mouse")
clock = pygame.time.Clock()

# Game classes
class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.width = 30
        self.height = 30
        
    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Keep bird on screen
        if self.y <= 0:
            self.y = 0
            self.velocity = 0
        
    def flap(self):
        self.velocity = FLAP_STRENGTH
    
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height), border_radius=10)
        
    def get_mask(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, 400)
        self.top_pipe = pygame.Rect(self.x, 0, 60, self.height)
        self.bottom_pipe = pygame.Rect(self.x, self.height + PIPE_GAP, 60, HEIGHT)
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x
        
    def draw(self):
        pygame.draw.rect(screen, GREEN, self.top_pipe)
        pygame.draw.rect(screen, GREEN, self.bottom_pipe)
        
    def collide(self, bird):
        bird_mask = bird.get_mask()
        return bird_mask.colliderect(self.top_pipe) or bird_mask.colliderect(self.bottom_pipe)

# Game variables
def reset_game():
    bird = Bird()
    pipes = []
    score = 0
    game_active = True
    last_pipe = pygame.time.get_ticks()
    return bird, pipes, score, game_active, last_pipe

# Font for score
font = pygame.font.SysFont('Arial', 30)

# Main game function
def main():
    bird, pipes, score, game_active, last_pipe = reset_game()
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        bird.flap()
                    else:
                        bird, pipes, score, game_active, last_pipe = reset_game()
        
        # Game logic (only if game is active)
        if game_active:
            # Update bird
            bird.update()
            
            # Generate pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe = time_now
            
            # Update and check pipes
            for pipe in pipes[:]:
                pipe.update()
                
                # Check collision
                if pipe.collide(bird):
                    game_active = False
                
                # Check if bird passed the pipe
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    score += 1
                
                # Remove pipes that are off-screen
                if pipe.x < -60:
                    pipes.remove(pipe)
            
            # Check if bird hits the ground or goes off the top
            if bird.y + bird.height >= HEIGHT - GROUND_HEIGHT or bird.y <= 0:
                game_active = False
        
        # Drawing
        # Background
        screen.fill(SKY_BLUE)
        
        # Draw pipes
        for pipe in pipes:
            pipe.draw()
        
        # Draw ground
        pygame.draw.rect(screen, BROWN, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
        
        # Draw bird
        bird.draw()
        
        # Score display
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Game over text
        if not game_active:
            game_over_text = font.render('Game Over! Press SPACE to restart', True, BLACK)
            screen.blit(game_over_text, (WIDTH//2 - 180, HEIGHT//2))
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 