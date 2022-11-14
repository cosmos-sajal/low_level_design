from game_board import Game
from player import Player
from playing_piece import PlayingPieceO, PlayingPieceX

# creating players
player1 = Player("Player 1", PlayingPieceO())
player2 = Player("Player 2", PlayingPieceX())

# initialising board
game = Game(3)
game.add_player(player1)
game.add_player(player2)
game.start_game()
