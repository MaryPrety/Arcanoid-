import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_SIZE = 20
BRICK_WIDTH, BRICK_HEIGHT = 75, 20
BRICK_ROWS = 5
BRICK_COLS = 10
MAX_LIVES = 3  # Количество жизней
FPS = 60  # Кадры в секунду
BRICK_SPACING = 10  # Промежуток между кирпичами

# Цвета
WHITE = (255, 255, 255)
PINK_TEXT = (249, 44, 133)  # Цвет текста #f92c85
BRICK_COLORS = [(155, 222, 172), (75, 190, 160), (80, 128, 114)]  # Цвета плиток
BALL_COLOR = (255, 227, 240)  # Цвет мяча #ffe3f0
BACKGROUND_COLOR = (47, 72, 88)  # Темно-синий фон #2f4858

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арканоид")

# Класс для кирпичей
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.hit = False
        self.color = random.choice(BRICK_COLORS)  # Случайный цвет плитки

# Класс для ракетки
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dx):
        self.rect.x += dx
        # Ограничение движения ракетки
        self.rect.x = max(0, min(self.rect.x, WIDTH - PADDLE_WIDTH))

# Класс для мяча
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.dx = 0
        self.dy = 0

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

# Функция для создания случайных кирпичей
def create_random_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = col * (BRICK_WIDTH + BRICK_SPACING) + BRICK_SPACING
            y = row * (BRICK_HEIGHT + BRICK_SPACING) + 50  # Появление кирпичей в верхней части экрана
            if y < HEIGHT - PADDLE_HEIGHT - BRICK_HEIGHT:
                bricks.append(Brick(x, y))
    return bricks

# Функция для отображения сообщения о завершении игры
def show_game_over_message(message):
    font = pygame.font.Font(None, 48)
    text = font.render(message, True, PINK_TEXT)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)
    menu()  # Возврат в меню после показа сообщения

# Функция для отображения сообщения о победе
def show_victory_message():
    show_game_over_message("Congratulations!")

# Меню завершенной игры с отметкой пройденного режима
def game_complete_menu(mode):
    font = pygame.font.Font(None, 48)
    complete_text = font.render(f"Режим {mode} завершен", True, PINK_TEXT)
    main_menu_text = font.render("Главное меню", True, PINK_TEXT)
    complete_rect = complete_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    main_menu_rect = main_menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Пробел - выбор
                    menu()
                    running = False

        screen.fill(BACKGROUND_COLOR)
        screen.blit(complete_text, complete_rect)
        screen.blit(main_menu_text, main_menu_rect)
        pygame.display.flip()

# Функция для отображения жизней
def draw_lives(lives):
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Lives: {'-' * lives}", True, PINK_TEXT)
    screen.blit(lives_text, (10, 10))

# Тестовый режим
def test_mode(sub_mode):
    ball1 = Ball(WIDTH // 4, HEIGHT // 2)
    ball2 = Ball(3 * WIDTH // 4 - BALL_SIZE, HEIGHT // 2)
    ball1.dx = 4
    ball2.dx = -4
    ball1.dy = ball2.dy = 0

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                    return

        ball1.move()
        ball2.move()

        # Проверка столкновений между мячами
        if ball1.rect.colliderect(ball2.rect):
            if sub_mode == "collision":
                ball1.dx, ball2.dx = ball2.dx, ball1.dx
                ball1.dy, ball2.dy = ball2.dy, ball1.dy
            elif sub_mode == "pass through":
                pass  # Мячи проходят сквозь друг друга

        # Проверка столкновений с границами
        if ball1.rect.x <= 0 or ball1.rect.x + BALL_SIZE >= WIDTH:
            ball1.dx = -ball1.dx
        if ball1.rect.y <= 0 or ball1.rect.y + BALL_SIZE >= HEIGHT:
            ball1.dy = -ball1.dy

        if ball2.rect.x <= 0 or ball2.rect.x + BALL_SIZE >= WIDTH:
            ball2.dx = -ball2.dx
        if ball2.rect.y <= 0 or ball2.rect.y + BALL_SIZE >= HEIGHT:
            ball2.dy = -ball2.dy

        # Обновление экрана
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.ellipse(screen, BALL_COLOR, ball1.rect)
        pygame.draw.ellipse(screen, BALL_COLOR, ball2.rect)
        pygame.display.flip()
        clock.tick(FPS)

# Главный игровой цикл
def main(mode):
    if mode == "test mode":
        test_mode_sub = menu_test_mode()
        if test_mode_sub:
            test_mode(test_mode_sub)
        return

    paddle = Paddle()
    ball = Ball(paddle.rect.centerx, paddle.rect.top - BALL_SIZE, random.choice([-4, 4]), -4)
    ball2 = None  # Второй мяч изначально отсутствует
    bricks = create_random_bricks()  # Создание случайных кирпичей
    lives = MAX_LIVES if mode == "easy" or mode == "fast" else 1  # Количество жизней зависит от режима
    running = True
    clock = pygame.time.Clock()
    bricks_destroyed = 0  # Счетчик разрушенных блоков
    ball_launched = False  # Флаг для запуска первого мяча
    ball2_launched = False  # Флаг для запуска второго мяча
    attempt = 1  # Номер попытки
    next_ball2_threshold = 6  # Порог для появления второго мяча
    ball_lost = False  # Флаг потери одного мяча (используется в режиме fast)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                    return
                elif event.key == pygame.K_SPACE:  # Пробел для запуска мяча
                    if not ball_launched:
                        ball.dx = random.choice([-4, 4])
                        ball.dy = -4
                        ball_launched = True
                    elif ball2 and not ball2_launched:
                        ball2.dx = random.choice([-4, 4])
                        ball2.dy = -4
                        ball2_launched = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-10)
            if not ball_launched:
                ball.rect.centerx = paddle.rect.centerx
        if keys[pygame.K_RIGHT]:
            paddle.move(10)
            if not ball_launched:
                ball.rect.centerx = paddle.rect.centerx

        # Движение мячей
        if ball_launched:
            ball.move()
        if ball2 and ball2_launched:
            ball2.move()

        # === Логика потери мяча и жизней ===
        if ball.rect.y >= HEIGHT:  # Если первый мяч потерян
            if mode == "easy":  # Простой режим: теряем одну жизнь сразу
                lives -= 1
                if lives > 0:
                    ball = Ball(paddle.rect.centerx, paddle.rect.top - BALL_SIZE, random.choice([-4, 4]), -4)
                    ball_launched = False
                else:
                    show_game_over_message("Game Over!")
                    running = False
            elif mode == "fast":  # Быстрый режим: жизни теряются по-другому
                if ball2 is None:  # Если второго мяча нет, теряем жизнь
                    lives -= 1
                    if lives > 0:
                        ball = Ball(paddle.rect.centerx, paddle.rect.top - BALL_SIZE, random.choice([-4, 4]), -4)
                        ball_launched = False
                    else:
                        show_game_over_message("Game Over!")
                        running = False
                else:  # Если есть второй мяч, не теряем жизнь сразу
                    ball_lost = True
                    ball_launched = False

        if ball2 and ball2.rect.y >= HEIGHT:  # Если второй мяч потерян
            if mode == "fast" and ball_lost:  # Если потеряны оба мяча
                lives -= 1
                ball2 = None
                ball_lost = False
                if lives > 0:
                    ball = Ball(paddle.rect.centerx, paddle.rect.top - BALL_SIZE, random.choice([-4, 4]), -4)
                    ball_launched = False
                else:
                    show_game_over_message("Game Over!")
                    running = False
            else:  # Если потерян только второй мяч
                ball2 = None

        if mode == "hard":  # Сложный режим: потеря любого мяча = конец игры
            if ball.rect.y >= HEIGHT or (ball2 and ball2.rect.y >= HEIGHT):
                lives -= 1
                show_game_over_message("Game Over!")
                running = False

        # Проверка столкновений с ракеткой
        if ball_launched and ball.rect.colliderect(paddle.rect):
            ball.bounce_y()
        if ball2 and ball2_launched and ball2.rect.colliderect(paddle.rect):
            ball2.bounce_y()

        # Логика появления второго мяча
        if bricks_destroyed >= next_ball2_threshold and ball2 is None and mode != "hard":
            ball2 = Ball(paddle.rect.centerx, paddle.rect.top - BALL_SIZE, random.choice([-4, 4]), -4)
            ball2_launched = False

        # Отображение объектов
        screen.fill(BACKGROUND_COLOR)
        draw_lives(lives)
        pygame.draw.rect(screen, WHITE, paddle.rect)
        pygame.draw.ellipse(screen, BALL_COLOR, ball.rect)
        if ball2:
            pygame.draw.ellipse(screen, BALL_COLOR, ball2.rect)
        for brick in bricks:
            pygame.draw.rect(screen, brick.color, brick.rect)

        pygame.display.flip()
        clock.tick(FPS)

        # Главный игровой цикл
def main(mode):
    if mode == "test mode":
        test_mode_sub = menu_test_mode()
        if test_mode_sub:
            test_mode(test_mode_sub)
        return

    paddle = Paddle()
    ball = Ball(paddle.rect.centerx, paddle.rect.top - BALL_SIZE)
    ball2 = None  # Второй мяч
    bricks = create_random_bricks()  # Создание случайных кирпичей
    lives = MAX_LIVES if mode == "easy" or mode == "fast" else 1  # Количество жизней
    running = True
    clock = pygame.time.Clock()
    bricks_destroyed = 0  # Счетчик разрушенных блоков
    ball_launched = False  # Флаг для запуска мяча
    ball2_launched = False  # Флаг для запуска второго мяча
    attempt = 1  # Номер попытки
    next_ball2_threshold = 6  # Порог для появления второго мяча

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                    return
                elif event.key == pygame.K_SPACE:  # Пробел для запуска мяча
                    if not ball_launched:
                        ball.dx = random.choice([-4, 4])
                        ball.dy = -4
                        ball_launched = True
                    elif ball2 and not ball2_launched:
                        ball2.dx = random.choice([-4, 4])
                        ball2.dy = -4
                        ball2_launched = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-10)
            if not ball_launched:
                ball.rect.centerx = paddle.rect.centerx
        if keys[pygame.K_RIGHT]:
            paddle.move(10)
            if not ball_launched:
                ball.rect.centerx = paddle.rect.centerx

        if ball_launched:
            ball.move()
        if ball2 and ball2_launched:
            ball2.move()

        # Проверка столкновений с кирпичами
        for brick in bricks[:]:
            if not brick.hit and ball.rect.colliderect(brick.rect):
                ball.dy = -ball.dy
                brick.hit = True
                bricks.remove(brick)  # Удаляем кирпич после попадания
                bricks_destroyed += 1
                if (mode == "fast" or mode == "hard") and bricks_destroyed >= next_ball2_threshold and not ball2:
                    ball2 = Ball(paddle.rect.centerx, paddle.rect.top - BALL_SIZE)  # Создаем второй мяч на платформе
                    ball2_launched = False
                    next_ball2_threshold += 6 * attempt  # Увеличиваем порог для следующего мяча

            if ball2 and not brick.hit and ball2.rect.colliderect(brick.rect):
                ball2.dy = -ball2.dy
                brick.hit = True
                bricks.remove(brick)  # Удаляем кирпич после попадания
                bricks_destroyed += 1

        # Проверка столкновений с ракеткой
        if ball.rect.colliderect(paddle.rect):
            ball.dy = -ball.dy
            ball.rect.bottom = paddle.rect.top  # Исправление лага
            if not ball_launched:
                ball.dx = random.choice([-4, 4])
                ball.dy = -4

        if ball2 and ball2.rect.colliderect(paddle.rect):
            ball2.dy = -ball2.dy
            ball2.rect.bottom = paddle.rect.top  # Исправление лага
            if not ball2_launched:
                ball2.dx = random.choice([-4, 4])
                ball2.dy = -4

        # Проверка столкновений между мячами
        if ball2 and ball.rect.colliderect(ball2.rect):
            if mode == "hard":
                ball.dx, ball2.dx = ball2.dx, ball.dx
                ball.dy, ball2.dy = ball2.dy, ball.dy
            elif mode == "fast":
                pass  # Мячи проходят сквозь друг друга

        # Проверка столкновений с границами
        if ball.rect.x <= 0 or ball.rect.x + BALL_SIZE >= WIDTH:
            ball.dx = -ball.dx
        if ball.rect.y <= 0:
            ball.dy = -ball.dy
        if ball.rect.y >= HEIGHT:
            lives -= 1
            ball_launched = False
            ball.rect.center = (paddle.rect.centerx, paddle.rect.top - BALL_SIZE)

        if ball2:
            if ball2.rect.x <= 0 or ball2.rect.x + BALL_SIZE >= WIDTH:
                ball2.dx = -ball2.dx
            if ball2.rect.y <= 0:
                ball2.dy = -ball2.dy
            if ball2.rect.y >= HEIGHT:
                ball2_launched = False
                ball2.rect.center = (paddle.rect.centerx, paddle.rect.top - BALL_SIZE)

        # Если жизни кончились
        if lives <= 0:
            show_game_over_message("Tempus Ineptum!")  # "Бессмысленное время" на латыни
            running = False

        # Если все кирпичи уничтожены
        if len(bricks) == 0:
            show_victory_message()
            running = False

        # Обновление экрана
        screen.fill(BACKGROUND_COLOR)
        draw_lives(lives)
        pygame.draw.rect(screen, WHITE, paddle.rect)
        pygame.draw.ellipse(screen, BALL_COLOR, ball.rect)
        if ball2:
            pygame.draw.ellipse(screen, BALL_COLOR, ball2.rect)

        for brick in bricks:
            pygame.draw.rect(screen, brick.color, brick.rect)

        pygame.display.flip()
        clock.tick(FPS)

# Главное меню
def menu():
    font = pygame.font.Font(None, 48)
    options = ["Easy", "Fast", "Hard", "Test Mode"]
    selected = 0

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        for i, option in enumerate(options):
            color = PINK_TEXT if i == selected else WHITE
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50 + i * 60))
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_SPACE:
                    mode = options[selected].lower()
                    if mode == "test mode":
                        menu_test_mode()  # Переход к выбору подрежима тестового режима
                    else:
                        main(mode)
                    running = False

def menu_test_mode():
    font = pygame.font.Font(None, 48)
    options = ["Collision", "Pass Through"]
    selected = 0

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        for i, option in enumerate(options):
            color = PINK_TEXT if i == selected else WHITE
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50 + i * 60))
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_SPACE:
                    if selected == 0:
                        test_mode("collision")
                    elif selected == 1:
                        test_mode("pass through")
                    running = False
                

menu()
pygame.quit()
