import pygame
import random
import sys

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
HUD_HEIGHT = 50
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = (WINDOW_HEIGHT - HUD_HEIGHT) // CELL_SIZE
SNAKE_SPEED = 5

BLACK = (10, 10, 15)
WHITE = (245, 245, 250)
DARK_GREEN = (20, 120, 40)
LIGHT_GREEN = (80, 220, 100)
RED = (255, 80, 80)
DARK_RED = (180, 30, 30)
BLUE = (60, 120, 200)
YELLOW = (255, 220, 50)
GRAY = (100, 100, 110)
GOLD = (255, 215, 0)
PURPLE = (147, 112, 219)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.game_state = 'START'
        self.reset_game()
        self.high_score = 0

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def draw_start_screen(self):
        self.screen.fill(BLACK)

        title = self.title_font.render('Snake Game', True, LIGHT_GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        instructions = [
            'Use arrow keys to control the snake',
            'Eat red food to score points',
            'Game over if you hit the wall or yourself',
            '',
            'Press any key to start'
        ]

        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 280 + i * 40))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def draw_game_over_screen(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.title_font.render('Game Over!', True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)

        score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 280))
        self.screen.blit(score_text, score_rect)

        if self.score > self.high_score:
            high_score_text = self.font.render('New Record!', True, YELLOW)
            high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, 330))
            self.screen.blit(high_score_text, high_score_rect)
            self.high_score = self.score

        restart_text = self.font.render('Press SPACE to restart', True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, 400))
        self.screen.blit(restart_text, restart_rect)

        quit_text = self.font.render('Press ESC to quit', True, GRAY)
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, 450))
        self.screen.blit(quit_text, quit_rect)

        pygame.display.flip()

    def draw_snake(self):
        for i, segment in enumerate(self.snake):
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE + HUD_HEIGHT
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            if i == 0:
                pygame.draw.rect(self.screen, LIGHT_GREEN, rect, border_radius=5)
                pygame.draw.rect(self.screen, WHITE, rect, 2, border_radius=5)

                eye_size = 6
                pupil_size = 3
                eye_offset = 5

                if self.direction == (1, 0):
                    left_eye = (rect.right - eye_offset - 3, rect.top + eye_offset)
                    right_eye = (rect.right - eye_offset - 3, rect.bottom - eye_offset)
                elif self.direction == (-1, 0):
                    left_eye = (rect.left + eye_offset + 3, rect.top + eye_offset)
                    right_eye = (rect.left + eye_offset + 3, rect.bottom - eye_offset)
                elif self.direction == (0, -1):
                    left_eye = (rect.left + eye_offset, rect.top + eye_offset + 3)
                    right_eye = (rect.right - eye_offset, rect.top + eye_offset + 3)
                else:
                    left_eye = (rect.left + eye_offset, rect.bottom - eye_offset - 3)
                    right_eye = (rect.right - eye_offset, rect.bottom - eye_offset - 3)

                pygame.draw.circle(self.screen, WHITE, left_eye, eye_size)
                pygame.draw.circle(self.screen, WHITE, right_eye, eye_size)
                pygame.draw.circle(self.screen, BLACK, left_eye, pupil_size)
                pygame.draw.circle(self.screen, BLACK, right_eye, pupil_size)

                pygame.draw.circle(self.screen, (255, 255, 255, 100), left_eye, eye_size + 1, 1)
                pygame.draw.circle(self.screen, (255, 255, 255, 100), right_eye, eye_size + 1, 1)
            else:
                color_intensity = max(60, 160 - i * 5)
                color = (30, min(220, color_intensity + 70), 50)
                pygame.draw.rect(self.screen, color, rect, border_radius=3)
                pygame.draw.rect(self.screen, DARK_GREEN, rect, 1, border_radius=3)

    def draw_food(self):
        x = self.food[0] * CELL_SIZE
        y = self.food[1] * CELL_SIZE + HUD_HEIGHT
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        center_x = rect.centerx
        center_y = rect.centery
        radius = CELL_SIZE // 2 - 1

        pygame.draw.circle(self.screen, RED, (center_x, center_y), radius)
        pygame.draw.circle(self.screen, DARK_RED, (center_x, center_y), radius, 2)

        highlight_x = center_x - 4
        highlight_y = center_y - 4
        pygame.draw.circle(self.screen, (255, 180, 180), (highlight_x, highlight_y), 3)

        pygame.draw.circle(self.screen, (255, 220, 220), (highlight_x + 1, highlight_y + 1), 2)

        leaf_x = center_x
        leaf_y = rect.top + 2
        pygame.draw.ellipse(self.screen, (50, 180, 50), (leaf_x - 4, leaf_y - 3, 8, 6))
        pygame.draw.line(self.screen, (30, 140, 30), (leaf_x, leaf_y + 1), (leaf_x, leaf_y + 4), 2)

    def draw_hud(self):
        pygame.draw.rect(self.screen, (25, 25, 35), (0, 0, WINDOW_WIDTH, HUD_HEIGHT))
        pygame.draw.line(self.screen, (80, 80, 90), (0, HUD_HEIGHT), (WINDOW_WIDTH, HUD_HEIGHT), 2)

        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (20, 10))

        high_score_text = self.small_font.render(f'High Score: {self.high_score}', True, GOLD)
        self.screen.blit(high_score_text, (WINDOW_WIDTH - 150, 15))

    def draw(self):
        if self.game_state == 'START':
            self.draw_start_screen()
        elif self.game_state == 'PLAYING':
            self.screen.fill(BLACK)

            self.draw_hud()

            for x in range(0, WINDOW_WIDTH, CELL_SIZE):
                pygame.draw.line(self.screen, (20, 20, 20), (x, HUD_HEIGHT), (x, WINDOW_HEIGHT))
            for y in range(HUD_HEIGHT, WINDOW_HEIGHT, CELL_SIZE):
                pygame.draw.line(self.screen, (20, 20, 20), (0, y), (WINDOW_WIDTH, y))

            self.draw_snake()
            self.draw_food()

            if self.game_over:
                self.draw_game_over_screen()

            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == 'START':
                    self.game_state = 'PLAYING'
                elif self.game_state == 'PLAYING':
                    if not self.game_over:
                        if event.key == pygame.K_UP and self.direction != (0, 1):
                            self.next_direction = (0, -1)
                        elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                            self.next_direction = (0, 1)
                        elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                            self.next_direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                            self.next_direction = (1, 0)

                    if event.key == pygame.K_SPACE and self.game_over:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
        return True

    def update(self):
        if self.game_state != 'PLAYING' or self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in self.snake):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(SNAKE_SPEED)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = SnakeGame()
    game.run()
