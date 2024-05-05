import random

import pygame

from exceptions import GameOverException


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

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
SPEED = 10

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

    def __init__(
            self,
            position=SCREEN_CENTER,
            body_color=BOARD_BACKGROUND_COLOR) -> None:
        """Init method"""
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """A method for future redefinition. Abstract"""
        raise NotImplementedError(
            "Method 'draw' must be implemented in subclasses."
        )

    def draw_cell(self, position) -> None:
        """Draw cell at screen"""
        rect = pygame.Rect(position, (GRID_SIZE,
                                      GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def paint_over(self, coords):
        """Paint over last element"""
        erase_rect = pygame.Rect(
            coords,
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(
            screen,
            BOARD_BACKGROUND_COLOR,
            erase_rect
        )


class Apple(GameObject):
    """A class describing an apple and actions with it"""

    def __init__(self) -> None:
        """Init method"""
        super().__init__(body_color=APPLE_COLOR)

        # Avoid position of center, cos in first rotation there is a snake
        self.randomize_position(
            occupied_positions=[SCREEN_CENTER]
        )

    def randomize_position(self, occupied_positions) -> None:
        """Set position attribute for object of class"""
        if len(occupied_positions) >= GRID_HEIGHT * GRID_WIDTH:
            raise GameOverException(message="Game Over")

        while self.position in occupied_positions:
            self.position = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

    def draw(self) -> None:
        """Draw an apple at screen"""
        self.draw_cell(self.position)


class Snake(GameObject):
    """A class describing a snake and actions with it"""

    def __init__(self):
        """Init method, add attribute of parent class to current"""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self):
        """The method of updating the direction after clicking on the button"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Method allows snake to move"""
        coord_x, coord_y = self.get_head_position

        coord_x = coord_x % SCREEN_WIDTH
        coord_y = coord_y % SCREEN_HEIGHT

        direction_x, direction_y = self.direction
        new_position = (
            coord_x + direction_x * GRID_SIZE,
            coord_y + direction_y * GRID_SIZE)
        self.positions.insert(0, new_position)
        if self.length <= len(self.positions):
            self.last = self.positions.pop()
        else:
            self.last = None

    @property
    def get_head_position(self):
        """Return first elements of list (head)"""
        return self.positions[0]

    def reset(self):
        """Reset the game"""
        self.length = 1
        self.direction = random.choice([
            UP,
            DOWN,
            RIGHT,
            LEFT
        ])
        self.last = None
        self.next_direction = None
        self.positions = [self.position]
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self):
        """Drow snake at the screen"""
        # Drow head
        self.draw_cell(self.get_head_position)

        # paint over last
        if self.last:
            self.paint_over(self.last)


def handle_keys(game_object):
    r"""Handle user's movements"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and (
                    game_object.direction != DOWN):
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and (
                    game_object.direction != UP):
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and (
                    game_object.direction != RIGHT):
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and (
                    game_object.direction != LEFT):
                game_object.next_direction = RIGHT


def main():
    """Main func"""
    # Initialize PyGame:
    pygame.init()
    # Create instance of class
    snake = Snake()
    apple = Apple()
    apple.draw()

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
            try:
                apple.randomize_position(snake.positions)
            except GameOverException:
                snake.reset()
            apple.draw()

        # If snake eat itself reset the game
        if snake.get_head_position in snake.positions[2:]:
            snake.reset()
            apple.draw()

        # Drow the game
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
