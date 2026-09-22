from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов
       Предоставляет общую структуру для хранения позиции и цвета.

    Attributes:
        position (tuple[int, int]): Список координат сегментов объекта.
        body_color (tuple[int, int, int]): Цвет объекта в формате RGB."""

    def __init__(self, body_color):
        self.body_color = body_color
        self.position = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

    def draw(self):
        """
        Метод отрисовки объекта на экране. 
        Метод переопределяется дочерними классами.
        """

        pass


class Apple(GameObject):
    """
    Игровой объект Яблоко.
    Отвечает за появление и отрисовку яблока на поле.
    """

    def __init__(self, body_color):
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self):
        rand_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        rand_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (rand_x, rand_y)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)        


class Snake(GameObject):
    """
    Игровой объект Змея.
    Отвечает за появление и отрисовку змеии на поле.
    """

    def __init__(self, body_color):
        super().__init__(body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def reset(self):
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        head_position = self.get_head_position()

        new_head_position_x = head_position[0] + self.direction[0] * GRID_SIZE
        new_head_position_y = head_position[1] + self.direction[1] * GRID_SIZE

        # Первый вариант изменения координат при выходе за границы поля.
        if new_head_position_x == 640 or new_head_position_x == -20:
            new_head_position_x = new_head_position_x % SCREEN_WIDTH

        elif new_head_position_y == 480 or new_head_position_y == -20:
            new_head_position_y = new_head_position_y % SCREEN_HEIGHT

        # Если первый вариант не будет работать, попробовать этот.
        # new_head_position_x = new_head_position_x % SCREEN_WIDTH
        # new_head_position_y = new_head_position_y % SCREEN_HEIGHT
        new_head_position = (new_head_position_x, new_head_position_y)

        self.positions.insert(0, new_head_position)
        self.last = self.positions[-1]
        # Удаляем последний сегмент, если не съели яблоко.
        if len(self.positions) > self.length:
            self.positions.remove(self.last)

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # Метод draw класса Snake
    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


# Функция обработки действий пользователя
def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def reset_screen():
    screen.fill(BOARD_BACKGROUND_COLOR)


def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple(APPLE_COLOR)
    snake = Snake(SNAKE_COLOR)

    while True:
        clock.tick(SPEED)
        reset_screen()
        # Обратбота событий клавиатуры.
        handle_keys(snake)
        # Обновление направления движения змейки.
        snake.update_direction()
        # Перемещение змейки.
        snake.move()
        # Проверяем съела ли яблоко.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        # Проверяем столкновение змейки с собой.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            reset_screen()
        # Отрисовка яблока и змеи.
        apple.draw()
        snake.draw()
        # Обновлене экрана
        pygame.display.update()


if __name__ == '__main__':
    main()
