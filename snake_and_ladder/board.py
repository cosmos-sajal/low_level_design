from cell import Cell
from jump import Jump, JumpType


class Board:
    def __init__(
        self,
        size_of_board,
        no_of_snakes,
        no_of_ladders
    ):
        self.size_of_board = size_of_board
        self.cells = []
        for i in range(0, size_of_board):
            cell = Cell(i + 1, None)
            self.cells.append(cell)

        self.create_jumps(no_of_ladders, no_of_snakes)

    def create_jumps(self, no_of_ladders, no_of_snakes):
        for i in range(0, no_of_ladders):
            jump = Jump(self.size_of_board, JumpType.LADDER)
            self.cells[jump.start_pos].jump = jump

        for i in range(0, no_of_snakes):
            jump = Jump(self.size_of_board, JumpType.SNAKE)
            self.cells[jump.start_pos].jump = jump
