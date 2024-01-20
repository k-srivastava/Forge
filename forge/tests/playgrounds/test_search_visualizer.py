from copy import copy
from enum import IntEnum

from forge.core.engine.color import Color
from forge.core.engine.display import Display
from forge.core.engine.game import Game
from forge.core.managers import keyboard
from forge.core.managers.keyboard import Key
from forge.core.physics.vector import Vector2D
from forge.hearth.elements.shapes import Line, Rectangle
from forge.hearth.elements.text import Text

MAX_ARRAY_LENGTH = 8
CELL_SIZE = 125
PADDING = 10
ARROW_LENGTH = 70
ARROW_WIDTH = 5

DEFAULT_CELL_COLOR = Color(255, 255, 255)
CURRENT_CELL_COLOR = Color(232, 214, 16)
CORRECT_CELL_COLOR = Color(0, 255, 0)
INCORRECT_CELL_COLOR = Color(255, 0, 0)


class VisualizerType(IntEnum):
    ALL = 1
    BINARY = 2
    LINEAR = 3


class Cell:
    def __init__(self, number: int, top_left: Vector2D) -> None:
        self.square = Rectangle(
            top_left, CELL_SIZE, CELL_SIZE, DEFAULT_CELL_COLOR, line_width=5
        )

        self.text = Text(str(number), Vector2D.zero(), 64)
        self.text.center = self.square.center

        self.square.add_to_renderer()
        self.text.add_to_renderer()


class Arrow:
    def __init__(self, top_center: Vector2D) -> None:
        self.offset: int = ARROW_LENGTH // 3

        self.vertical_line = Line(
            copy(top_center), Vector2D(top_center.x, top_center.y + ARROW_LENGTH),
            DEFAULT_CELL_COLOR, width=ARROW_WIDTH
        )

        self.left_line = Line(
            Vector2D(top_center.x - self.offset, top_center.y + self.offset), copy(top_center),
            DEFAULT_CELL_COLOR, width=ARROW_WIDTH
        )

        self.right_line = Line(
            copy(top_center), Vector2D(top_center.x + self.offset, top_center.y + self.offset),
            DEFAULT_CELL_COLOR, width=ARROW_WIDTH
        )

        self.vertical_line.add_to_renderer()
        self.left_line.add_to_renderer()
        self.right_line.add_to_renderer()

    def move_to(self, top_center: Vector2D) -> None:
        self.vertical_line.start_point = copy(top_center)
        self.vertical_line.end_point = Vector2D(top_center.x, top_center.y + ARROW_LENGTH)

        self.left_line.start_point = Vector2D(top_center.x - self.offset, top_center.y + self.offset)
        self.left_line.end_point = copy(top_center)

        self.right_line.start_point = copy(top_center)
        self.right_line.end_point = Vector2D(top_center.x + self.offset, top_center.y + self.offset)

    def move_offset(self, top_left: Vector2D, offset: int) -> None:
        self.move_to(
            Vector2D(top_left.x + ((CELL_SIZE + PADDING) * offset) + (CELL_SIZE // 2), top_left.y + CELL_SIZE + PADDING)
        )


class Array:
    def __init__(self, top_left: Vector2D, *numbers: int) -> None:
        self.top_left = top_left
        self.cells: list[Cell] = []
        self.arrow = Arrow(Vector2D(self.top_left.x + (CELL_SIZE // 2), self.top_left.y + CELL_SIZE + PADDING))

        delta_x = 0

        for number in numbers:
            self.cells.append(Cell(number, Vector2D(self.top_left.x + delta_x, self.top_left.y)))
            delta_x += CELL_SIZE + PADDING


class LinearSearchVisualizerTest(Game):
    def __init__(self, number_to_find: int, *numbers: int) -> None:
        super().__init__(Display(title='Linear Search Visualizer Tests'))

        self.number_to_find = number_to_find
        self.numbers: tuple[int, ...] = numbers

        self.current_index = 0
        self.number_found = False

        self.top_left = Vector2D(100, 400)
        self.array = Array(self.top_left, *numbers)

        self.title = Text('Linear Search', Vector2D.zero(), 128)
        self.title.center = Vector2D(self.display.width() // 2, self.display.height() // 2 - 250)

        self.number_text = Text(
            f'Number: {self.number_to_find}', Vector2D(100, self.title.top_left.y + 200), 32
        )

        self.current_index_text = Text(
            f'Current Index: {self.current_index}', Vector2D(100, self.number_text.top_left.y + 50), 32
        )

        self.num_comparisons_text = Text(f'Number of Comparisons: {self.current_index + 1}', Vector2D.zero(), 32)
        self.num_comparisons_text.center = Vector2D(self.display.width() // 2, self.display.height() // 2 - 100)

        self.number_found_text = Text('', Vector2D.zero(), 32)

        self.title.add_to_renderer()
        self.number_text.add_to_renderer()
        self.current_index_text.add_to_renderer()
        self.num_comparisons_text.add_to_renderer()

        self.update_array_colors()

    def update_array_colors(self) -> None:
        if self.number_found:
            return

        for idx, cell in enumerate(self.array.cells):
            if idx == self.current_index:
                cell.square.color = CURRENT_CELL_COLOR

            elif idx > self.current_index:
                cell.square.color = DEFAULT_CELL_COLOR

            else:
                cell.square.color = INCORRECT_CELL_COLOR

    def update(self) -> None:
        if self.number_found or self.current_index == len(self.numbers):
            if self.number_found:
                self.number_found_text.text = f'Number found at index {self.current_index}.'

            elif self.current_index == len(self.numbers):
                self.number_found_text.text = 'Number not found.'

            self.number_found_text.center = Vector2D(self.display.width() // 2, self.display.height() - 70)
            self.number_found_text.add_to_renderer()

            super().update()
            return

        if keyboard.is_clicked(Key.SPACE) and self.current_index < len(self.numbers):
            current_cell = self.array.cells[self.current_index]

            if current_cell.text.text == str(self.number_to_find):
                current_cell.square.color = CORRECT_CELL_COLOR
                self.number_found = True

            if not self.number_found:
                self.current_index += 1

                self.current_index_text.text = f'Current Index: {self.current_index}'
                self.num_comparisons_text.text = f'Number of Comparisons: {self.current_index + 1}'

                self.array.arrow.move_offset(self.top_left, self.current_index)
                self.update_array_colors()

        super().update()


class BinarySearchVisualizerTset(Game):
    def __init__(self, number_to_find: int, *numbers: int) -> None:
        super().__init__(Display(title='Binary Search Visualizer Tests'))

        self.number_to_find = number_to_find
        self.numbers: tuple[int, ...] = numbers

        self.number_found = False

        self.top_left = Vector2D(100, 400)
        self.array = Array(self.top_left, *numbers)

        self.start = 0
        self.end = len(numbers) - 1
        self.middle = (self.start + self.end) // 2
        self.visited_cells: list[int] = []

        self.title = Text('Binary Search', Vector2D.zero(), 128)
        self.title.center = Vector2D(self.display.width() // 2, self.display.height() // 2 - 250)

        self.number_text = Text(
            f'Number: {self.number_to_find}', Vector2D(100, self.title.top_left.y + 200), 32
        )

        self.middle_index_text = Text(
            f'Middle Index: {self.middle}', Vector2D(100, self.number_text.top_left.y + 50), 32
        )

        self.start_index_text = Text(
            f'Start Index: {self.start}', Vector2D(self.display.width() - 350, self.title.top_left.y + 200), 32
        )

        self.end_index_text = Text(
            f'End Index: {self.end}', Vector2D(self.display.width() - 350, self.number_text.top_left.y + 50), 32
        )

        self.num_comparisons_text = Text(f'Number of Comparisons: {len(self.visited_cells) + 1}', Vector2D.zero(), 32)
        self.num_comparisons_text.center = Vector2D(self.display.width() // 2, self.display.height() // 2 - 100)

        self.number_found_text = Text('', Vector2D.zero(), 32)

        self.title.add_to_renderer()
        self.number_text.add_to_renderer()

        self.middle_index_text.add_to_renderer()
        self.start_index_text.add_to_renderer()
        self.end_index_text.add_to_renderer()

        self.num_comparisons_text.add_to_renderer()

        self.array.arrow.move_offset(self.top_left, self.middle)
        self.update_array_colors()

    def update_array_colors(self) -> None:
        if self.number_found:
            return

        self.visited_cells.append(self.middle)

        for idx, cell in enumerate(self.array.cells):
            if idx == self.middle:
                cell.square.color = CURRENT_CELL_COLOR

            if idx in self.visited_cells:
                cell.square.color = INCORRECT_CELL_COLOR

    def update(self) -> None:
        if self.number_found or self.start >= self.end:
            if self.number_found:
                self.number_found_text.text = f'Number found at index {self.middle}.'

            elif self.start >= self.end:
                self.number_found_text.text = 'Number not found.'

            self.number_found_text.center = Vector2D(self.display.width() // 2, self.display.height() - 70)
            self.number_found_text.add_to_renderer()

            super().update()
            return

        if keyboard.is_clicked(Key.SPACE):  # and self.current_index < len(self.numbers):
            current_cell = self.array.cells[self.middle]

            if current_cell.text.text == str(self.number_to_find):
                current_cell.square.color = CORRECT_CELL_COLOR
                self.number_found = True

            if not self.number_found:
                if current_cell.text.text < str(self.number_to_find):
                    self.start = self.middle + 1
                    self.start_index_text.text = f'Start Index: {self.start}'

                else:
                    self.end = self.middle - 1
                    self.end_index_text.text = f'End Index: {self.end}'

                self.middle = (self.start + self.end) // 2

                self.middle_index_text.text = f'Middle Index: {self.middle}'
                self.num_comparisons_text.text = f'Number of Comparisons: {len(self.visited_cells) + 1}'

                self.array.arrow.move_offset(self.top_left, self.middle)
                self.update_array_colors()

        super().update()


def main() -> None:
    array_length: int

    while True:
        array_length = int(input('Enter the length of the array: '))

        if 1 <= array_length <= MAX_ARRAY_LENGTH:
            break
        else:
            print(f'Invalid array length of {array_length}. Try again.\n')

    numbers: list[int] = []

    print()
    for i in range(array_length):
        numbers.append(int(input(f'Enter the {i}th number: ')))

    number_to_find = int(input('\nEnter the number to be found: '))

    visualizer_type: VisualizerType

    print()
    while True:
        type_ = input('Which type of visualization: linear, binary or all?\n1. All\n2. Binary\n3. Linear\n> ').lower()

        if type_ in ('1', '2', '3', 'a', 'all', 'b', 'binary', 'l', 'linear'):
            if type_ in ('1', 'a', 'all'):
                visualizer_type = VisualizerType.ALL

            elif type_ in ('2', 'b', 'binary'):
                visualizer_type = VisualizerType.BINARY

            else:
                visualizer_type = VisualizerType.LINEAR

            break

        else:
            print('Invalid input! Try again.\n')

    match visualizer_type:
        case VisualizerType.ALL:
            print('Running linear search visualizer...')
            linear_search_visualizer_test = LinearSearchVisualizerTest(number_to_find, *numbers)
            linear_search_visualizer_test.mainloop()

            if not sorted(numbers) == numbers:
                print('Sorting the numbers for binary search.')

            numbers = sorted(numbers)

            print('Running binary search visualizer...')
            binary_search_visualizer_test = BinarySearchVisualizerTset(number_to_find, *numbers)
            binary_search_visualizer_test.mainloop()

        case VisualizerType.BINARY:
            print('Running binary search visualizer...')

            if not sorted(numbers) == numbers:
                print('Sorting the numbers for binary search.')

            numbers = sorted(numbers)

            binary_search_visualizer_test = BinarySearchVisualizerTset(number_to_find, *numbers)
            binary_search_visualizer_test.mainloop()

        case VisualizerType.LINEAR:
            if not sorted(numbers) == numbers:
                print('Sorting the numbers for binary search.')

            numbers = sorted(numbers)

            print('Running linear search visualizer...')
            linear_search_visualizer_test = LinearSearchVisualizerTest(number_to_find, *numbers)
            linear_search_visualizer_test.mainloop()


if __name__ == '__main__':
    main()
