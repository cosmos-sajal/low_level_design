from player import Player
from dice import Dice
from board import Board


class Game:
    def __init__(
        self,
        size_of_board,
        no_of_snakes,
        no_of_ladders
    ):
        self.players = [
            Player("Player 1"),
            Player("Player 2"),
            Player("Player 3"),
            Player("Player 4")
        ]
        self.player_turn = 0
        self.dice = Dice()
        self.board = Board(size_of_board, no_of_snakes, no_of_ladders)
        self.size_of_board = size_of_board

    def __move_player_for_snake_or_ladder(self, current_pos):
        jump = self.board.cells[current_pos].jump
        if jump is None:
            return

        self.players[self.player_turn].current_position = jump.end_pos
        if current_pos > jump.end_pos:
            print(f"Player has been bitten by snake, current position now is - {jump.end_pos}")
        else:
            print(f"Player has climbed a ladder, current position now is - {jump.end_pos}")

    def __change_turn(self):
        self.player_turn += 1
        if self.player_turn >= len(self.players):
            self.player_turn = 0

    def __remove_other_player_if_already_on_cell(self):
        current_player_iterator = self.player_turn
        for i in range(0, len(self.players)):
            if i == current_player_iterator:
                continue

            if self.players[i].current_position == \
                    self.players[current_player_iterator].current_position:
                self.players[i].current_position = 0
                print(f"{self.players[i].name} has reached the starting point")
                break

    def __did_player_win(self):
        if self.players[self.player_turn].current_position == \
                self.size_of_board - 1:
            return True
        else:
            return False

    def start_game(self):
        while True:
            print("----------------------")
            print(f"{self.players[self.player_turn].name}'s Turn")
            print(f"Current Position: {self.players[self.player_turn].current_position}")
            dice_value = self.dice.roll_dice()
            print(f"Dice Rolled: Dice value is {dice_value}")
            if self.players[self.player_turn].current_position + \
                    dice_value >= self.size_of_board:
                print("Overshot, next player's turn")
                self.__change_turn()
                continue

            self.players[self.player_turn].current_position += dice_value

            self.__move_player_for_snake_or_ladder(
                self.players[self.player_turn].current_position)

            self.__remove_other_player_if_already_on_cell()

            if self.__did_player_win():
                print(f"{self.players[self.player_turn].name} Won, Game Over")
                break

            print(f"Current Position Now is - {self.players[self.player_turn].current_position}")

            self.__change_turn()
