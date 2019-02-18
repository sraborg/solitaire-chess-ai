from bitarray import bitarray
from enum import Enum, unique


class Chessboard:


    def __init__(self, rows=3, columns=3):
        self._rows = rows
        self._columns = columns
        self._num_of_spaces = rows * columns
        self._board = bitarray(self._num_of_spaces)
        self._board.setall(0)

        self._location = {}

        self._last_square_bit = 2**(self._num_of_spaces - 1)

    def add_piece(self, position_index, piece):
        try:
            if not self._valid_board_space(position_index):
                raise ValueError("Invalid Location")

            elif not isinstance(piece, Piece):
                raise ValueError("Invalid Piece")

            else:
                self._board[position_index - 1] = True
                self._location[position_index] = piece

        except ValueError:
            raise

    def print_board(self):
        board_string = self._board.to01()[::-1]

        for x in range(0, self._rows):
            start = x * self._columns
            end = start + self._columns
            row_string = slice(start, end)
            print(board_string[row_string][::-1])

    def print_pieces(self):
        for k,v in self._location.items():
            print(v.name, "at position", k)

    def getRow(self,position_index):
        if self._valid_board_space(position_index):
            return ((position_index-1) % self._rows) +1
        else:
            print("Invalid Location")

    def _valid_board_space(self, position_index):
        if position_index > 0 and position_index <= self._num_of_spaces:
            return True
        else:
            return False

    def _generate_psuedo_attacks(self):
        self._generate_pawn_pseudo_attacks()
        self._generate_knight_pseudo_attacks()
        self._generate_rook_pseudo_attacks()
        self._generate_bishop_pseudo_attacks()
        self._generate_queen_pseudo_attacks()
        self._generate_king_pseudo_attacks()

    def _generate_pawn_pseudo_attacks(self):
        pass

    def _generate_knight_pseudo_attacks(self):
        pass

    def _generate_rook_pseudo_attacks(self):
        pass

    def _generate_bishop_pseudo_attacks(self):
        pass

    def _generate_queen_pseudo_attacks(self):
        pass

    def _generate_king_pseudo_attacks(self):
        pass

@unique
class Piece(Enum):
    BISHOP = 1
    KING = 2
    KNIGHT = 3
    ROOK = 4
    PAWN = 5
    QUEEN = 6

board = Chessboard(4, 3)

board.add_piece(4, Piece.BISHOP)
board.add_piece(1, Piece.KNIGHT)
board.add_piece(3, Piece.QUEEN)
board.add_piece(9, Piece.ROOK)
board.print_pieces()
board.print_board()


