from enum import Enum


class Piece(Enum):
    PieceX = 'X'
    PieceO = 'O'


class PlayingPiece:
    def __init__(self, piece_type):
        self.piece_type = piece_type


class PlayingPieceX(PlayingPiece):
    def __init__(self):
        super().__init__(Piece.PieceX.value)


class PlayingPieceO(PlayingPiece):
    def __init__(self):
        super().__init__(Piece.PieceO.value)
