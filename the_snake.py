# 3-rd party imports
from random import choice, randint
import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -20)
DOWN = (0, 20)
LEFT = (-20, 0)
RIGHT = (20, 0)

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
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """
    The base class from which other game objects are inherited.
    It contains common attributes of game objects.
    ABSTRACT
    """

    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
    color = None

    def __init__(self, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
                                 ), body_color=None) -> None:
        """Init method"""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """A method for future redefinition. Abstract"""
        pass


class Apple(GameObject):
    """A class describing an apple and actions with it"""

    def __init__(self) -> None:
        """Init method"""
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self) -> tuple:
        """Set position attribute for object of class"""
        self.position = (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE)
        return self.position

    def draw(self, screen) -> None:
        """Draw an apple at screen"""
        rect = pygame.Rect(self.position, (GRID_SIZE,
                                           GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """A class describing a snake and actions with it"""

    length = 1
    positions = []
    direction = RIGHT
    next_direction = None
    body_color = SNAKE_COLOR

    def __init__(self):
        """Init method, add attribute of parent class to current"""
        self.positions.append(super().position)
        self.last = None

    def update_direction(self):
        """The method of updating the direction after clicking on the button"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    @staticmethod
    def clear_coordinates(coord):
        """Return filtered coordinates within allowed game board"""
        coord_x = coord[0]
        coord_y = coord[1]

        allowed_x = range(0, SCREEN_WIDTH, 20)
        allowed_y = range(0, SCREEN_HEIGHT, 20)

        if coord_x not in allowed_x:
            if coord_x < 0:
                coord_x += SCREEN_WIDTH
            else:
                coord_x -= SCREEN_WIDTH

        if coord_y not in allowed_y:
            if coord_y < 0:
                coord_y += SCREEN_HEIGHT
            else:
                coord_y -= SCREEN_HEIGHT

        return (coord_x, coord_y)

    def move(self):
        """Method allows snake to move"""
        current_pos = self.get_head_position

        self.positions.insert(0, self.clear_coordinates((
            current_pos[0] + self.direction[0],
            current_pos[1] + self.direction[1])))
        if self.length <= __class__.length:
            self.last = self.positions[-1]
            self.positions.pop()
        self.length = __class__.length

    @property
    def get_head_position(self):
        """Return first elements of list (head)"""
        return self.positions[0]

    def reset(self):
        """Reset the game"""
        self.length = 1
        self.direction = choice([
            UP,
            DOWN,
            RIGHT,
            LEFT
        ])
        self.positions = [__class__.position]

    def draw(self, screen):
        """Drow snake at the screen"""
        for position in self.positions[1:]:
            rect = (pygame.Rect(position, (GRID_SIZE,
                                           GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Drow head
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE,
                                GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # paint over last
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE,
                                                GRID_SIZE))
            pygame.draw.rect(
                screen,
                BOARD_BACKGROUND_COLOR,
                last_rect)


def handle_keys(game_object):
    r"""Handle user's movements"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and\
                    (game_object.direction != DOWN):
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and\
                    (game_object.direction != UP):
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and\
                    (game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and\
                    (game_object.direction != LEFT):
                game_object.next_direction = RIGHT


def main():
    """Main func"""
    # Initialize PyGame:
    pygame.init()
    # Create instance of class
    snake = Snake()
    apple = Apple()

    while True:
        # Set speed of snake
        clock.tick(SPEED)
        handle_keys(snake)
        # Movements
        snake.update_direction()
        snake.move()
        # if snake reaches apple position increment length
        if snake.get_head_position == apple.position:
            snake.length += 1  # increment length
            while True:
                position = apple.randomize_position()
                axis_x = range(0, SCREEN_WIDTH)
                axis_y = range(0, SCREEN_HEIGHT)
                valid_position = (position[0] in axis_x) \
                    and (position[1] in axis_y)
                # if position of apple in a corrent position
                if position not in snake.positions and valid_position:
                    break

        # If snake eat itself reset the game
        if snake.get_head_position in snake.positions[2:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        # Drow the game
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
