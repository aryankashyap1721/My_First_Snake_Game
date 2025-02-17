import pygame
import time
import random
import os

# Initialize pygame and mixer for sound
pygame.init()
pygame.mixer.init()

# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Game settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20
GAME_SPEED = 15

# Initialize the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Advanced Snake Game')

# Initialize fonts
title_font = pygame.font.SysFont("arial", 72)
menu_font = pygame.font.SysFont("arial", 36)
score_font = pygame.font.SysFont("arial", 24)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + (x*BLOCK_SIZE)) % WINDOW_WIDTH, (cur[1] + (y*BLOCK_SIZE)) % WINDOW_HEIGHT)
        if new in self.positions[3:]:
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True
            
    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (
            random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE,
            random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        )
        
    def render(self, surface):
        pygame.draw.rect(surface, self.color, 
                        (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# Directional constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def load_high_score():
    try:
        with open("high_score.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("high_score.txt", "w") as f:
        f.write(str(score))

def main_menu():
    high_score = load_high_score()
    
    while True:
        screen.fill(BLACK)
        title_text = title_font.render("SNAKE GAME", True, GREEN)
        start_text = menu_font.render("Press SPACE to Start", True, WHITE)
        quit_text = menu_font.render("Press Q to Quit", True, WHITE)
        high_score_text = menu_font.render(f"High Score: {high_score}", True, YELLOW)
        
        screen.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, 100))
        screen.blit(start_text, (WINDOW_WIDTH//2 - start_text.get_width()//2, 300))
        screen.blit(quit_text, (WINDOW_WIDTH//2 - quit_text.get_width()//2, 350))
        screen.blit(high_score_text, (WINDOW_WIDTH//2 - high_score_text.get_width()//2, 250))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_q:
                    return False

def game_loop():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    high_score = load_high_score()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                if event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                if event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                if event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
                    
        if not snake.update():
            break
            
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 10
            food.randomize_position()
            
        screen.fill(BLACK)
        snake.render(screen)
        food.render(screen)
        
        score_text = score_font.render(f"Score: {snake.score}", True, WHITE)
        high_score_text = score_font.render(f"High Score: {high_score}", True, YELLOW)
        screen.blit(score_text, (5, 5))
        screen.blit(high_score_text, (5, 25))
        
        pygame.display.update()
        clock.tick(GAME_SPEED)
    
    if snake.score > high_score:
        save_high_score(snake.score)
    
    return snake.score

def game_over_screen(score):
    high_score = load_high_score()
    
    while True:
        screen.fill(BLACK)
        game_over_text = title_font.render("GAME OVER", True, RED)
        score_text = menu_font.render(f"Score: {score}", True, WHITE)
        high_score_text = menu_font.render(f"High Score: {high_score}", True, YELLOW)
        retry_text = menu_font.render("Press SPACE to Retry", True, WHITE)
        quit_text = menu_font.render("Press Q to Quit", True, WHITE)
        
        screen.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, 100))
        screen.blit(score_text, (WINDOW_WIDTH//2 - score_text.get_width()//2, 250))
        screen.blit(high_score_text, (WINDOW_WIDTH//2 - high_score_text.get_width()//2, 300))
        screen.blit(retry_text, (WINDOW_WIDTH//2 - retry_text.get_width()//2, 400))
        screen.blit(quit_text, (WINDOW_WIDTH//2 - quit_text.get_width()//2, 450))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_q:
                    return False

def main():
    while True:
        if not main_menu():
            break
        score = game_loop()
        if not game_over_screen(score):
            break
            
    pygame.quit()

if __name__ == "__main__":
    main()
