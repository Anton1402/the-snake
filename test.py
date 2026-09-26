from the_snake import Snake

snake = Snake((0, 255, 0))


def get_needed_amount(snake, *objects):
    for obj in objects:
        if obj == 'bad_food':
            obj.need_amount = snake.max_length // 5
        elif obj == 'stones':
            obj.need_amount = snake.max_length // 7



def comparison_with_needed_amt(*objects):
    for obj in objects:
        if len(obj.positions) < obj.needed_amount:
            obj.randomize_position()


def get_occupied_positions(objects):
    """
    Возвращает список координат занятых клеток.

    Args:
        objects (list[GameObject]):
            Игровые объекты, занимающие клетки поля.

    Returns:
        list[tuple[int, int]]:
            Координаты всех занятых клеток.
    """
    occupied_positions = []

    for obj in objects:
        if isinstance(obj, Apple):
            occupied_positions.append(obj.position)
        else:
            occupied_positions.extend(obj.positions)

    return occupied_positions
