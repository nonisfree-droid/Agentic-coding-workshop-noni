import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
FPS = 60

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
STAR_COLOR = (200, 200, 255)
COLORS = [
    (0, 255, 255),    # Cyan - I
    (0, 0, 255),      # Blue - J
    (255, 165, 0),    # Orange - O
    (255, 255, 0),    # Yellow - S
    (0, 255, 0),      # Green - T
    (255, 0, 0),      # Red - Z
    (128, 0, 128),    # Purple - L
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
]

class Starfield:
    def __init__(self):
        self.stars = []
        for _ in range(150):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.5, 2.5),
                'size': random.randint(1, 3)
            })
    
    def update(self):
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > SCREEN_HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, screen):
        for star in self.stars:
            pygame.draw.circle(screen, STAR_COLOR, (int(star['x']), int(star['y'])), star['size'])

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Space Tetris - Galaxy Edition')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        
        self.starfield = Starfield()
        self.reset_game()
        
    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.fall_time = 0
        self.fall_speed = 0.8
        
    def new_piece(self):
        shape = random.choice(SHAPES)
        color = COLORS[SHAPES.index(shape)]
        return {
            'shape': shape,
            'color': color,
            'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
            'y': 0,
            'rotation': 0
        }
    
    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(
                        self.screen,
                        self.grid[y][x],
                        (x * GRID_SIZE + 100, y * GRID_SIZE + 50, GRID_SIZE - 1, GRID_SIZE - 1)
                    )
    
    def draw_piece(self, piece, offset_x=0, offset_y=0):
        shape = piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        piece['color'],
                        ((piece['x'] + x + offset_x) * GRID_SIZE + 100,
                         (piece['y'] + y + offset_y) * GRID_SIZE + 50,
                         GRID_SIZE - 1, GRID_SIZE - 1)
                    )
    
    def draw_next_piece(self):
        shape = self.next_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        self.next_piece['color'],
                        (x * GRID_SIZE + 500, y * GRID_SIZE + 100, GRID_SIZE - 1, GRID_SIZE - 1)
                    )
    
    def draw_ui(self):
        # Score
        score_text = self.small_font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (500, 250))
        
        # Level
        level_text = self.small_font.render(f'Level: {self.level}', True, WHITE)
        self.screen.blit(level_text, (500, 300))
        
        # Lines
        lines_text = self.small_font.render(f'Lines: {self.lines_cleared}', True, WHITE)
        self.screen.blit(lines_text, (500, 350))
        
        # Next piece label
        next_text = self.small_font.render('Next:', True, WHITE)
        self.screen.blit(next_text, (500, 50))
    
    def draw_game_over(self):
        if self.game_over:
            game_over_text = self.font.render('GAME OVER', True, (255, 100, 100))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            
            restart_text = self.small_font.render('Press R to Restart', True, (200, 200, 255))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
            
            title_text = self.small_font.render('Space Tetris - Galaxy Edition', True, (150, 150, 255))
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
    
    def valid_move(self, piece, dx=0, dy=0, rotated_shape=None):
        shape = rotated_shape if rotated_shape else piece['shape']
        new_x = piece['x'] + dx
        new_y = piece['y'] + dy
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    if (new_x + x < 0 or new_x + x >= GRID_WIDTH or
                        new_y + y >= GRID_HEIGHT or
                        (new_y + y >= 0 and self.grid[new_y + y][new_x + x])):
                        return False
        return True
    
    def rotate_piece(self, piece):
        # Transpose and reverse to rotate
        shape = piece['shape']
        rotated = [[shape[j][i] for j in range(len(shape))] for i in range(len(shape[0]) - 1, -1, -1)]
        return rotated
    
    def lock_piece(self):
        shape = self.current_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    if self.current_piece['y'] + y >= 0:
                        self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']
        
        # Check for cleared lines
        lines_to_clear = []
        for i, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                lines_to_clear.append(i)
        
        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        # Update score
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            self.score += len(lines_to_clear) * 100 * self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(0.1, 0.8 - (self.level - 1) * 0.05)
        
        # New piece
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        
        if not self.valid_move(self.current_piece):
            self.game_over = True
    
    def update(self, dt):
        if self.game_over:
            return
            
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            if self.valid_move(self.current_piece, dy=1):
                self.current_piece['y'] += 1
            else:
                self.lock_piece()
            self.fall_time = 0
    
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset_game()
                    else:
                        if event.key == pygame.K_LEFT:
                            if self.valid_move(self.current_piece, dx=-1):
                                self.current_piece['x'] -= 1
                        elif event.key == pygame.K_RIGHT:
                            if self.valid_move(self.current_piece, dx=1):
                                self.current_piece['x'] += 1
                        elif event.key == pygame.K_DOWN:
                            if self.valid_move(self.current_piece, dy=1):
                                self.current_piece['y'] += 1
                        elif event.key == pygame.K_UP:
                            rotated = self.rotate_piece(self.current_piece)
                            if self.valid_move(self.current_piece, rotated_shape=rotated):
                                self.current_piece['shape'] = rotated
                        elif event.key == pygame.K_SPACE:
                            while self.valid_move(self.current_piece, dy=1):
                                self.current_piece['y'] += 1
                            self.lock_piece()
            
            self.update(dt)
            
            # Draw space background
            self.screen.fill(BLACK)
            self.starfield.update()
            self.starfield.draw(self.screen)
            
            # Draw game grid
            # Draw grid border
            pygame.draw.rect(self.screen, (50, 50, 100), 
                           (99, 49, GRID_WIDTH * GRID_SIZE + 2, GRID_HEIGHT * GRID_SIZE + 2), 2)
            
            self.draw_grid()
            self.draw_piece(self.current_piece)
            self.draw_next_piece()
            self.draw_ui()
            self.draw_game_over()
            
            pygame.display.flip()

if __name__ == '__main__':
    game = Tetris()
    game.run()