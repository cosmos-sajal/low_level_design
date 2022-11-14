class PrintGameBoard:
    def print_board(self, board, size):
        for i in range(0, size):
            for j in range(0, size):
                if board[i][j] is None:
                    print("-", end="    ")
                else:
                    print(board[i][j].piece_type, end="    ")
            print("")


class Game:
    def __init__(self, size):
        self.size_of_board = size
        self.board = [[None for i in range(size)] for j in range(size)]
        self.players = []
        self.player_turn = 0
        self.move_count = 0
        self.print_game_board = PrintGameBoard()

    def __can_play_this_turn(self, pos_x, pos_y):
        if self.size_of_board <= pos_x or \
                self.size_of_board <= pos_y:
            return False
        elif self.board[pos_x][pos_y] is None:
            return True

        return False

    def __play_move(self, pos_x, pos_y, player):
        self.board[pos_x][pos_y] = player.playing_piece
        self.move_count += 1

    def __change_turn(self):
        self.player_turn = 1 - self.player_turn

    def __is_any_move_left(self):
        return self.move_count < self.size_of_board * self.size_of_board

    def __did_player_win(self):
        # check all horizontal tiles -
        for i in range(0, self.size_of_board):
            did_win = True
            for j in range(0, self.size_of_board - 1):
                if self.board[i][j] is None or self.board[i][j + 1] is None:
                    did_win = False
                    break
                elif self.board[i][j].piece_type != \
                        self.board[i][j + 1].piece_type:
                    did_win = False
                    break
            if did_win:
                return True

        if did_win:
            return True

        # check all vertical tiles -
        for i in range(0, self.size_of_board):
            did_win = True
            for j in range(0, self.size_of_board - 1):
                if self.board[j][i] is None or self.board[j + 1][i] is None:
                    did_win = False
                    break
                elif self.board[j][i].piece_type != \
                        self.board[j + 1][i].piece_type:
                    did_win = False
                    break
            if did_win:
                return True

        if did_win:
            return True

        # check 1st diagonal -
        did_win = True
        for i in range(0, self.size_of_board - 1):
            if self.board[i][i] is None or self.board[i + 1][i + 1] is None:
                did_win = False
                break
            elif self.board[i][i].piece_type != \
                    self.board[i + 1][i + 1].piece_type:
                did_win = False
                break

        if did_win:
            return True

        # check 2nd diagonal -
        did_win = True
        for i in range(self.size_of_board - 1, 0, -1):
            if self.board[i][i] is None or self.board[i - 1][i - 1] is None:
                did_win = False
                break
            elif self.board[i][i].piece_type != \
                    self.board[i - 1][i - 1].piece_type:
                did_win = False
                break

        return did_win

    def add_player(self, player):
        self.players.append(player)

    def start_game(self):
        while True:
            self.print_game_board.print_board(
                self.board, self.size_of_board)
            print(f"{self.players[self.player_turn].name}'s turn")
            pos_x, pos_y = \
                input("Enter the position you want to place:").split()
            pos_x, pos_y = int(pos_x), int(pos_y)

            if not self.__can_play_this_turn(pos_x, pos_y):
                print("Invalid position, please try again")
                continue

            self.__play_move(
                pos_x, pos_y, self.players[self.player_turn])

            if self.__did_player_win():
                self.print_game_board.print_board(
                    self.board, self.size_of_board)
                print(f"Game Over, {self.players[self.player_turn].name} won!")
                break

            if not self.__is_any_move_left():
                print("Game Tied")
                break

            self.__change_turn()
