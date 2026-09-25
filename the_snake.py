from random import choice, randint
from typing import TypeAlias

import pygame as pg

# Алиасы типов:
Direction: TypeAlias = tuple[int, int]
Color: TypeAlias = tuple[int, int, int]

# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP: Direction = (0, -1)
DOWN: Direction = (0, 1)
LEFT: Direction = (-1, 0)
RIGHT: Direction = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: Color = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: Color = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: Color = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: Color = (0, 255, 0)

# Цвет камня - серый:
STONE_COLOR: Color = (128, 128, 128)

# Скорость движения змейки:
SPEED: int = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс для игровых объектов
    Предоставляет общую структуру для хранения позиции и цвета.

    Attributes:
        position (tuple[int, int]): Список координат сегментов объекта.
                                    Изначально - центр экрана.
        body_color (Color): Цвет объекта в формате RGB.
    """

    def __init__(self, body_color: Color = STONE_COLOR):
        """Инициализация объекта класса GameObject.

        Args:
            body_color (Color): Цвет в формате RGB.
        """
        self.body_color = body_color
        self.position = (GRID_WIDTH // 2 * GRID_SIZE,
                         GRID_HEIGHT // 2 * GRID_SIZE)

    def draw(self):
        """
        Метод отрисовки объекта на экране.
        Метод переопределяется дочерними классами.
        """
        pass


class Apple(GameObject):
    """
    Игровой объект Яблоко. Наследуется от класса GameObject.
    Отвечает за появление и отрисовку яблока на поле.

    Attributes:
        body_color (Color): Цвет объекта в формате RGB.
        position ([tuple[int, int]): позиция яблока на игровом поле.

    Methods:
        __init__(self, snake_positions: tuple): Инициализация объекта.
        randomize_position(self, snake_positions: tuple):
            Устанавливает случайное положение яблока на игровом поле.
        draw(self): Отрисовка объекта на поле.
    """

    def __init__(
            self,
            body_color: Color = APPLE_COLOR,
            occupied_positions: list[tuple[int, int]] | None = None,
    ):
        """
        Инициализация объекта класса Apple.

        Args:
            body_color (Color): Цвет в формате RGB.
            occupied_positions (list[tuple[int, int]] | None):
                Текущие занятые координаты поля.
        """
        super().__init__(body_color=body_color)
        if occupied_positions is None:
            occupied_positions = []
        self.randomize_position(occupied_positions)

    def randomize_position(
            self,
            occupied_positions: list[tuple[int, int]],
    ):
        """
        Устанавливает случайное положение яблока на игровом поле.

        Args:
            occupied_positions (list[tuple[int, int]]):
                Координаты занятых клеток поля.
        """
        while True:
            rand_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            rand_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (rand_x, rand_y)
            # Проверка новых координат яблока на совпадение
            # с координатами змеи.
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовка яблока на поле."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Игровой объект Змея. Наследуется от класса GameObject.
    Отвечает за появление и отрисовку змеии на поле.

    Attributes:
        body_color (Color): Цвет змейки в формате RGB.
        length (int): Длина змейки.
        positions (list[tuple[int, int]]):
            Список позиций всех сегментов змейки.
        direction (tuple[int, int]):
            Направление движения змейки.
        next_direction (tuple[int, int] | None):
            Следующее направление движения, которое будет применено
            после обработки нажатия клавиши.

    Methods:
        __init__(self):
            Инициализирует объект класса.
        start_attributes(self):
            Задает начальное состояние аттрибутов змейки.
        reset(self):
            Возвращает змею в начальное состояние после столкновения.
        get_head_position(self):
            Возвращает координаты головы змеи.
        move(self):
            Перемещает змею на одну клетку в текущем направлении.
        get_new_head_position(self):
            Рассчитывает координаты головы змеи после следующего шага.
        update_direction(self):
            Обновляет направление движения змеи.
        draw(self): Отрисовывает змею на игровом поле.
    """

    def __init__(self, body_color: Color = SNAKE_COLOR):
        """Инициализация объекта класса Snake."""
        super().__init__(body_color=body_color)
        self.reset()

    def reset(self):
        """
        Возвращает змею в начальное состояние и
        задает случайное направление движения.
        """
        self.length = 1
        self.positions = [self.position]
        self.next_direction = None
        self.direction = RIGHT
        self.is_moving = False

    def get_head_position(self):
        """
        Возвращает координаты головы змеи.

        Returns:
            tuple[int, int]: Координаты головы змеи на игровом поле.
        """
        return self.positions[0]

    def move(self):
        """
        Перемещает змею на одну клетку в текущем направлении.
        Добавляет новую позицию головы в начало списка координат и удаляет
        последний сегмент, если длина змеи не увеличилась.
        """
        new_head_position = self.get_new_head_position()
        # Добавляем новые координаты головы.
        self.positions.insert(0, new_head_position)

        # Удаляем последний сегмент, если не съели яблоко.
        if len(self.positions) > self.length:
            self.positions.pop()

    def get_new_head_position(self):
        """
        Рассчитывает координаты головы змеи после следующего шага.
        Учитывает текущее направление движения и размер клетки.
        При выходе за границы игрового поля переносит змею на противоположную
        сторону поля.

        Returns:
            tuple[int, int]: Новые координаты головы змеи.
        """
        head_position = self.get_head_position()

        new_head_position_x = head_position[0] + self.direction[0] * GRID_SIZE
        new_head_position_y = head_position[1] + self.direction[1] * GRID_SIZE
        # Проход змейки сквозь границы поля.
        new_head_position_x %= SCREEN_WIDTH
        new_head_position_y %= SCREEN_HEIGHT

        return (new_head_position_x, new_head_position_y)

    def update_direction(self):
        """
        Обновляет направление движения змеи.
        Устанавливает новое направление, выбранное пользователем,
        если оно было задано.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
            self.is_moving = True

    def draw(self):
        """
        Отрисовывает змею на игровом поле.
        Сначала отрисовывает тело змеи, затем её голову.
        """
        # Отрисовка тела змейки
        for position in self.positions[1:]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)


def handle_keys(game_object):
    """
    Обрабатывает события ввода (нажатия клавиш) и устанавливает запланированное
    направление движения в game_object.next_direction.

    Args:
        game_object: Объект, состояние которого обновляется.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if not game_object.is_moving:
                if event.key == pg.K_UP:
                    game_object.next_direction = UP
                elif event.key == pg.K_DOWN:
                    game_object.next_direction = DOWN
                elif event.key == pg.K_LEFT:
                    game_object.next_direction = LEFT
                elif event.key == pg.K_RIGHT:
                    game_object.next_direction = RIGHT
            else:
                if event.key == pg.K_UP and game_object.direction != DOWN:
                    game_object.next_direction = UP
                elif event.key == pg.K_DOWN and game_object.direction != UP:
                    game_object.next_direction = DOWN
                elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                    game_object.next_direction = LEFT
                elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                    game_object.next_direction = RIGHT


def reset_screen():
    """
    Очищает игровое поле и заполняет его цветом фона.

    Используется перед каждой новой отрисовкой игрового состояния,
    чтобы удалить предыдущие изображения игровых объектов.
    """
    screen.fill(BOARD_BACKGROUND_COLOR)


def main():
    """
    Запускает основной игровой цикл.

    Функция выполняет следующие шаги:
        1) Инициализирует библиотеку PyGame и игровые объекты,
        2) Обрабатывает пользовательский ввод, проверяет поедание яблока.
        3) Перемещает змею, проверяет столкновения и
           отрисовывает текущее состояние игры.
    """
    # Инициализация PyGame:
    pg.init()
    # Тут нужно создать экземпляры классов.
    # Создаем сначала змею, так как в яблоко будут переданы координаты змейки.
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)
        reset_screen()
        # Обратбота событий клавиатуры.
        handle_keys(snake)
        # Обновление направления движения змейки.
        snake.update_direction()
        # Если змейя движется:
        if snake.is_moving:
            # Проверяем съела ли яблоко и увеличиваем длину.
            ate_apple = snake.get_new_head_position() == apple.position
            if ate_apple:
                snake.length += 1
            # Перемещение змейки.
            snake.move()
            # Новое яблоко теперь учитывает координаты новой головы змеи.
            if ate_apple:
                apple.randomize_position(snake.positions)
            # Проверяем столкновение змейки с собой.
            if snake.get_head_position() in snake.positions[1:]:
                snake.reset()
                # После сброса создаём яблоко заново,
                # чтобы оно не оказалось на змейке.
                apple.randomize_position(snake.positions)
        # Отрисовка яблока и змеи.
        apple.draw()
        snake.draw()
        # Обновлене экрана
        pg.display.update()


if __name__ == '__main__':
    main()
