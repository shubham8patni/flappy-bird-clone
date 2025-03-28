import pygame
import sys
import random
import math

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
WATER_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
SKY_BLUE = (135, 206, 235)
WATER_BLUE = (64, 164, 223)
FISH_ORANGE = (255, 140, 0)
CLOUD_WHITE = (240, 240, 240)

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FlappyFish")
clock = pygame.time.Clock()

# Game classes
class Fish:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.width = 40
        self.height = 25
        self.flip = False  # For fish animation
        self.flip_timer = 0
        
    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Keep fish on screen
        if self.y <= 0:
            self.y = 0
            self.velocity = 0
        
        # Fish animation
        self.flip_timer += 1
        if self.flip_timer > 10:
            self.flip = not self.flip
            self.flip_timer = 0
    
    def flap(self):
        self.velocity = FLAP_STRENGTH
        self.flip = not self.flip  # Flip the fish when flapping
    
    def draw(self):
        # Draw fish body
        pygame.draw.ellipse(screen, FISH_ORANGE, (self.x, self.y, self.width, self.height))
        
        # Draw tail
        tail_points = [
            (self.x, self.y + self.height//2),
            (self.x - 15, self.y + self.height//4),
            (self.x - 15, self.y + 3*self.height//4)
        ]
        pygame.draw.polygon(screen, FISH_ORANGE, tail_points)
        
        # Draw eye
        pygame.draw.circle(screen, WHITE, (self.x + self.width - 10, self.y + self.height//3), 5)
        pygame.draw.circle(screen, BLACK, (self.x + self.width - 10, self.y + self.height//3), 2)
        
        # Draw fin (flipping up and down)
        fin_height = 8 if self.flip else -8
        fin_points = [
            (self.x + self.width//3, self.y),
            (self.x + self.width//2, self.y - fin_height),
            (self.x + 2*self.width//3, self.y)
        ]
        pygame.draw.polygon(screen, FISH_ORANGE, fin_points)
        
    def get_mask(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Cloud:
    def __init__(self):
        self.x = WIDTH + random.randint(10, 100)
        self.y = random.randint(50, 200)
        self.width = random.randint(60, 120)
        self.height = random.randint(30, 50)
        self.speed = random.uniform(0.5, 1.5)
        
    def update(self):
        self.x -= self.speed
        
    def draw(self):
        # Draw a fluffy cloud using multiple circles
        radius = self.height // 2
        centers = [
            (self.x, self.y),
            (self.x + radius, self.y - radius//2),
            (self.x + radius*2, self.y),
            (self.x + radius//2, self.y + radius//3),
            (self.x + radius*1.5, self.y + radius//3)
        ]
        for center in centers:
            pygame.draw.circle(screen, CLOUD_WHITE, center, radius)

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
        # Draw pipes with a more interesting shape
        # Top pipe
        pygame.draw.rect(screen, GREEN, self.top_pipe)
        # Add pipe end cap
        pygame.draw.rect(screen, GREEN, (self.x - 5, self.height - 20, 70, 20))
        
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, self.bottom_pipe)
        # Add pipe end cap
        pygame.draw.rect(screen, GREEN, (self.x - 5, self.height + PIPE_GAP, 70, 20))
        
    def collide(self, fish):
        fish_mask = fish.get_mask()
        return fish_mask.colliderect(self.top_pipe) or fish_mask.colliderect(self.bottom_pipe)

class WaterSurface:
    def __init__(self):
        self.height = WATER_HEIGHT
        self.wave_offset = 0
        self.wave_points = []
        self.update_wave_points()
        
    def update(self):
        self.wave_offset += 0.1
        if self.wave_offset > 10:
            self.wave_offset = 0
        self.update_wave_points()
        
    def update_wave_points(self):
        self.wave_points = []
        for x in range(0, WIDTH + 10, 10):
            y = HEIGHT - self.height + math.sin(x/50 + self.wave_offset) * 5
            self.wave_points.append((x, y))
        # Add bottom corners to complete the polygon
        self.wave_points.append((WIDTH, HEIGHT))
        self.wave_points.append((0, HEIGHT))
        
    def draw(self):
        # Draw water surface with waves
        pygame.draw.polygon(screen, WATER_BLUE, self.wave_points)
        
        # Add some water highlights
        for x in range(20, WIDTH, 80):
            y = HEIGHT - self.height + 20
            pygame.draw.ellipse(screen, (100, 200, 255, 100), (x, y, 40, 10))

# Game variables
def reset_game():
    fish = Fish()
    pipes = []
    clouds = [Cloud() for _ in range(3)]  # Start with 3 clouds
    water = WaterSurface()
    score = 0
    game_active = True
    last_pipe = pygame.time.get_ticks()
    last_cloud = pygame.time.get_ticks()
    return fish, pipes, clouds, water, score, game_active, last_pipe, last_cloud

# Font for score
font = pygame.font.SysFont('Arial', 30)

# Main game function
def main():
    fish, pipes, clouds, water, score, game_active, last_pipe, last_cloud = reset_game()
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        fish.flap()
                    else:
                        fish, pipes, clouds, water, score, game_active, last_pipe, last_cloud = reset_game()
        
        # Game logic (only if game is active)
        if game_active:
            # Update fish
            fish.update()
            
            # Update water
            water.update()
            
            # Generate pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe = time_now
            
            # Generate clouds occasionally
            if time_now - last_cloud > 3000:  # Every 3 seconds
                if random.random() < 0.5:  # 50% chance
                    clouds.append(Cloud())
                last_cloud = time_now
            
            # Update clouds
            for cloud in clouds[:]:
                cloud.update()
                # Remove clouds that are off-screen
                if cloud.x + cloud.width < 0:
                    clouds.remove(cloud)
            
            # Update and check pipes
            for pipe in pipes[:]:
                pipe.update()
                
                # Check collision
                if pipe.collide(fish):
                    game_active = False
                
                # Check if fish passed the pipe
                if not pipe.passed and pipe.x < fish.x:
                    pipe.passed = True
                    score += 1
                
                # Remove pipes that are off-screen
                if pipe.x < -60:
                    pipes.remove(pipe)
            
            # Check if fish hits the water surface
            if fish.y + fish.height >= HEIGHT - WATER_HEIGHT:
                game_active = False
        
        # Drawing
        # Background
        screen.fill(SKY_BLUE)
        
        # Draw clouds
        for cloud in clouds:
            cloud.draw()
        
        # Draw pipes
        for pipe in pipes:
            pipe.draw()
        
        # Draw water
        water.draw()
        
        # Draw fish
        fish.draw()
        
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