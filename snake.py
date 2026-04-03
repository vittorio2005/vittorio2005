import sys
import random
import pygame

# Settaggio Gioco
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 60
START_SPEED = 10

# Colori
BG = (20, 22, 25)
GRID = (32, 35, 40)
SNAKE = (80, 210, 120)
SNAKE_HEAD = (100, 240, 140)
FOOD = (220, 80, 90)
TEXT = (230, 230, 230)

DIR_VECTORS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


def random_food(snake):
    while True:
        pos = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        if pos not in snake:
            return pos


def reset_game():
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    food = random_food(snake)
    score = 0
    speed = START_SPEED
    game_over = False
    return snake, direction, food, score, speed, game_over


def draw_grid(surface):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRID, (0, y), (WIDTH, y))


def draw_cell(surface, color, pos):
    rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake - pygame")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    snake, direction, food, score, speed, game_over = reset_game()
    move_timer = 0.0
    paused = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        move_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    snake, direction, food, score, speed, game_over = reset_game()
                    move_timer = 0.0
                    paused = False
                elif event.key in DIR_VECTORS and not game_over:
                    new_dir = DIR_VECTORS[event.key]
                    # Prevent reversing directly into itself
                    if len(snake) == 1 or (new_dir[0] != -direction[0] or new_dir[1] != -direction[1]):
                        direction = new_dir

        if not paused and not game_over:
            step_time = 1.0 / speed
            if move_timer >= step_time:
                move_timer -= step_time
                head_x, head_y = snake[0]
                new_head = (head_x + direction[0], head_y + direction[1])

                # Wall collision
                if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
                    game_over = True
                # Self collision
                elif new_head in snake:
                    game_over = True
                else:
                    snake.insert(0, new_head)
                    if new_head == food:
                        score += 1
                        speed = min(20, speed + 0.5)
                        food = random_food(snake)
                    else:
                        snake.pop()

        screen.fill(BG)
        draw_grid(screen)

        draw_cell(screen, FOOD, food)
        for i, segment in enumerate(snake):
            draw_cell(screen, SNAKE_HEAD if i == 0 else SNAKE, segment)

        score_text = font.render(f"Score: {score}", True, TEXT)
        screen.blit(score_text, (10, 8))
    
        if paused:
            step_timer = 0.0
            move_timer = step_timer
            pause_text = font.render("Pausa (Space)", True, TEXT)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 40))

        if game_over:
            over_text = font.render("Game Over - premi R per giocare di nuovo", True, TEXT)
            screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
