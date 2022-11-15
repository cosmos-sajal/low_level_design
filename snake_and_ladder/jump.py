import random
from enum import Enum


class JumpType(Enum):
    SNAKE = 0
    LADDER = 1


class Jump:
    def __init__(
        self,
        size_of_board,
        jump_type
    ):
        self.start_pos = None
        self.end_pos = None
        self.create_jump(
            size_of_board,
            jump_type
        )

    def create_jump(
        self,
        size_of_board,
        jump_type
    ):
        while True:
            start = random.randrange(size_of_board)
            end = random.randrange(size_of_board)
            if (jump_type == JumpType.LADDER and start >= end) or \
                    (jump_type == JumpType.SNAKE and start <= end):
                continue

            self.start_pos = start
            self.end_pos = end
            break
