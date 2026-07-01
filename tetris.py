import pygame
import random
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
FPS = 60

# Colors - bright kid-friendly colors
BG_COLOR = (135, 206, 235)  # Sky blue
BIRD_COLOR = (255, 255, 100)  # Yellow bird
WORM_COLOR = (100, 255, 100)   # Green worm
WHITE = (255, 255, 255)
COLORS = [
    (255, 100, 100),    # Red - I
    (255, 165, 0),      # Orange - J
    (255, 255, 100),    # Yellow - O
    (100, 255, 100),    # Green - S
    (100, 200, 255),    # Light blue - T
    (255, 100, 255),    # Pink - Z
    (255, 200, 100),    # Peach - L
]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
]

class Bird:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(50, 300)
        self.size = random.randint(20, 40)
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-0.5, 0.5)
        self.wing = 0
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.wing += 0.2
        if self.x < -50: self.x = SCREEN_WIDTH + 50
        if self.x > SCREEN_WIDTH + 50: self.x = -50
        if self.y < 30: self.y = 30
        if self.y > 300: self.y = 300
    
    def draw(self, screen):
        # Bird body
        pygame.draw.circle(screen, BIRD_COLOR, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (255, 200, 0), (int(self.x), int(self.y)), self.size, 2)
        # Wing
        wing_offset = int(5 * (1 if (self.wing % 1) > 0.5 else -1))
        pygame.draw.circle(screen, (255, 220, 50), (int(self.x - 8), int(self.y + wing_offset)), self.size // 2)
        # Eye
        pygame.draw.circle(screen, WHITE, (int(self.x + 8), int(self.y - 8)), 5)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + 9), int(self.y - 7)), 2)

class Worm:
    def __init__(self):
        self.x = random.randint(100, 700)
        self.y = SCREEN_HEIGHT - 30
        self.length = random.randint(20, 40)
        self.segments = []
        self.speed = random.uniform(0.5, 1.5)
        for i in range(self.length):
            self.segments.append({'x': self.x - i * 5, 'y': self.y})
    
    def update(self):
        # Move head
        self.segments[0]['x'] += self.speed
        if self.segments[0]['x'] > SCREEN_WIDTH + 20:
            self.segments[0]['x'] = -20
        
        # Follow segments
        for i in range(1, len(self.segments)):
            prev = self.segments[i-1]
            curr = self.segments[i]
            dist = ((prev['x'] - curr['x'])**2 + (prev['y'] - curr['y'])**2)**0.5
            if dist > 5:
                curr['x'] += (prev['x'] - curr['x']) * 0.1
                curr['y'] += (prev['y'] - curr['y']) * 0.1
    
    def draw(self, screen):
        for i, seg in enumerate(self.segments):
            size = max(3, 8 - abs(i - len(self.segments)//2) // 3)
            color = (max(50, 255 - i * 3), min(255, 150 + i * 2), max(50, 200 - i))
            pygame.draw.circle(screen, color, (int(seg['x']), int(seg['y'])), size)

class RoundedRect:
    @staticmethod
    def draw(screen, color, rect, radius=8):
        x, y, w, h = rect
        pygame.draw.rect(screen, color, (x + radius, y, w - 2*radius, h))
        pygame.draw.rect(screen, color, (x, y + radius, w, h - 2*radius))
        pygame.draw.circle(screen, color, (x + radius, y + radius), radius)
        pygame.draw.circle(screen, color, (x + w - radius, y + radius), radius)
        pygame.draw.circle(screen, color, (x + radius, y + h - radius), radius)
        pygame.draw.circle(screen, color, (x + w - radius, y + h - radius), radius)

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Kid Friendly Tetris!')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        
        self.birds = [Bird() for _ in range(5)]
        self.worms = [Worm() for _ in range(2)]
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
                    rect = (x * GRID_SIZE + 100, y * GRID_SIZE + 50, GRID_SIZE - 4, GRID_SIZE - 4)
                    RoundedRect.draw(self.screen, self.grid[y][x], rect, 6)
    
    def draw_piece(self, piece, offset_x=0, offset_y=0):
        shape = piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = ((piece['x'] + x + offset_x) * GRID_SIZE + 100,
                            (piece['y'] + y + offset_y) * GRID_SIZE + 50,
                            GRID_SIZE - 4, GRID_SIZE - 4)
                    RoundedRect.draw(self.screen, piece['color'], rect, 6)
    
    def draw_next_piece(self):
        shape = self.next_piece['shape']
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = (x * GRID_SIZE + 500, y * GRID_SIZE + 100, GRID_SIZE - 4, GRID_SIZE - 4)
                    RoundedRect.draw(self.screen, self.next_piece['color'], rect, 6)
    
    def draw_ui(self):
        score_text = self.small_font.render(f'Score: {self.score}', True, (255, 50, 100))
        self.screen.blit(score_text, (500, 250))
        
        level_text = self.small_font.render(f'Level: {self.level}', True, (50, 150, 255))
        self.screen.blit(level_text, (500, 300))
        
        lines_text = self.small_font.render(f'Lines: {self.lines_cleared}', True, (255, 150, 50))
        self.screen.blit(lines_text, (500, 350))
        
        next_text = self.small_font.render('Next:', True, (255, 150, 255))
        self.screen.blit(next_text, (500, 50))
    
    def draw_game_over(self):
        if self.game_over:
            game_over_text = self.font.render('GAME OVER!', True, (255, 50, 100))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            
            restart_text = self.small_font.render('Press R to Play Again!', True, (100, 200, 255))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    
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
        
        lines_to_clear = []
        for i, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                lines_to_clear.append(i)
        
        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            self.score += len(lines_to_clear) * 100 * self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(0.1, 0.8 - (self.level - 1) * 0.05)
        
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
            
            # Draw sky background
            self.screen.fill(BG_COLOR)
            
            # Draw sun
            pygame.draw.circle(self.screen, (255, 255, 100), (SCREEN_WIDTH - 80, 80), 50)
            
            # Update and draw birds
            for bird in self.birds:
                bird.update()
                bird.draw(self.screen)
            
            # Draw ground
            pygame.draw.rect(self.screen, (100, 200, 100), (0, SCREEN_HEIGHT - 25, SCREEN_WIDTH, 25))
            
            # Update and draw worms
            for worm in self.worms:
                worm.update()
                worm.draw(self.screen)
            
            # Draw game grid
            pygame.draw.rect(self.screen, (255, 200, 100), 
                           (99, 49, GRID_WIDTH * GRID_SIZE + 2, GRID_HEIGHT * GRID_SIZE + 2), 3)
            
            self.draw_grid()
            self.draw_piece(self.current_piece)
            self.draw_next_piece()
            self.draw_ui()
            self.draw_game_over()
            
            pygame.display.flip()

if __name__ == '__main__':
    game = Tetris()
    game.run()