
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
pygame.display.set_caption("Простой Арканоид")

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
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
        self.dx = random.choice([-4, 4])
        self.dy = -4

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

# Функция для создания случайных кирпичей
def create_random_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            # Расчет позиции кирпича с учетом промежутков
            x = col * (BRICK_WIDTH + BRICK_SPACING) + BRICK_SPACING
            y = row * (BRICK_HEIGHT + BRICK_SPACING) + 50  # Появление кирпичей в верхней части экрана
            if y < HEIGHT - PADDLE_HEIGHT - BRICK_HEIGHT:  # Убедиться, что кирпичи не слишком близко к платформе
                bricks.append(Brick(x, y))
    return bricks

# Функция для отображения сообщения о завершении игры
def show_game_over_message():
    font = pygame.font.Font(None, 48)
    text = font.render("Inane et sine fine", True, PINK_TEXT)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Задержка 3 секунды

# Главный игровой цикл
def main():
    paddle = Paddle()
    ball = Ball()
    bricks = create_random_bricks()  # Создание случайных кирпичей
    lives = MAX_LIVES
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-10)
        if keys[pygame.K_RIGHT]:
            paddle.move(10)

        ball.move()

        # Проверка столкновений с кирпичами
        for brick in bricks:
            if not brick.hit and ball.rect.colliderect(brick.rect):
                ball.dy = -ball.dy
                brick.hit = True
                bricks.remove(brick)  # Удаляем кирпич после попадания
                if not bricks:  # Если все кирпичи разбиты
                    show_game_over_message()
                    running = False

        # Проверка столкновений с ракеткой
        if ball.rect.colliderect(paddle.rect):
            ball.dy = -ball.dy

        # Проверка столкновений с границами
        if ball.rect.x <= 0 or ball.rect.x >= WIDTH - BALL_SIZE:
            ball.dx = -ball.dx
        if ball.rect.y <= 0:
            ball.dy = -ball.dy
        if ball.rect.y >= HEIGHT:
            lives -= 1  # Уменьшаем количество жизней
            ball = Ball()  # Перезапускаем мяч
            if lives <= 0:
                running = False  # Игра окончена

        # Отрисовка
        screen.fill(BACKGROUND_COLOR)  # Отрисовка фона
        for brick in bricks:
            if not brick.hit:
                pygame.draw.rect(screen, brick.color, brick.rect)  # Отрисовка плиток
        pygame.draw.rect(screen, PINK_TEXT, paddle.rect)  # Платформа #f92c85
        pygame.draw.ellipse(screen, BALL_COLOR, ball.rect)  # Отрисовка мяча

        # Отображение римских цифр в обратном порядке
        roman_numerals = "III" if lives == 3 else "II" if lives == 2 else "I" if lives == 1 else ""
        font = pygame.font.Font(None, 36)
        roman_text = font.render(roman_numerals, True, PINK_TEXT)
        screen.blit(roman_text, (WIDTH // 2 - roman_text.get_width() // 2, 10))  # Центрирование текста

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
