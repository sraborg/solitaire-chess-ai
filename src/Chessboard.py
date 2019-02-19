from bitarray import bitarray
from enum import Enum, unique, auto
import math
from ExtendedBitArray import ExtendedBitArray as ebs


class Chessboard:

    def __init__(self, rows=3, columns=3):
        self._rows = rows
        self._columns = columns
        self._num_of_spaces = rows * columns
        self._board = ebs(self._num_of_spaces)
        self._board.setall(0)

        self._location = {}
        self._rules = {}

        self._generate_psuedo_attacks()

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

    def is_valid_attack(self, source_location, target_location):
        try:
            source_piece = self._location.get(source_location)
            if source_piece == None:
                raise ValueError("Invalid Source Location")

            if self._location.get(target_location) == None:
                raise ValueError("Invalid Target Location")

            index = (Rules.PSEUDO_ATTACKS, source_piece, source_location)
            attack_board = self._rules[index]
            test_board = attack_board & self._board
            return test_board[target_location-1]
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

    def row(self, position_index):
        try:
            if not self._valid_board_space(position_index):
                raise ValueError("Invalid Location")
            else:
                index = self._num_of_spaces - (position_index -1)
                return math.ceil(index / self._columns)
        except ValueError:
            raise

    def column(self, position_index):
        try:
            if not self._valid_board_space(position_index):
                raise ValueError("Invalid Location")
            else:
                return ((position_index-1) % self._columns) +1
        except ValueError:
            raise

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
        pawn_psuedo_attacks = ebs(self._num_of_spaces)

        for x in range(1, self._num_of_spaces + 1):
            pawn_psuedo_attacks.setall(0)

            if self.row(x) == 1:
                self._rules[(Rules.PSEUDO_ATTACKS, Piece.PAWN, x)] = pawn_psuedo_attacks
            else:
                if not self.column(x) == 1:
                    pawn_psuedo_attacks[x + self._columns - 2] = True
                if not self.column(x) == self._columns:
                    pawn_psuedo_attacks[x + self._columns ] = True
                    pass
                self._rules[(Rules.PSEUDO_ATTACKS, Piece.PAWN, x)] = pawn_psuedo_attacks.copy()

    def _generate_knight_pseudo_attacks(self):
        knight_psuedo_attacks = ebs(self._num_of_spaces)

        for x in range(1, self._num_of_spaces + 1):
            knight_psuedo_attacks.setall(0)

            if not self.row(x) == 1:
                if self.column(x) > 2:
                    knight_psuedo_attacks[x + self._columns - 3] = True
                if self.column(x) < (self._columns - 1):
                    knight_psuedo_attacks[x + self._columns + 1] = True
                if not self.row(x) == 2:
                    if not self.column(x) == 1:
                        knight_psuedo_attacks[x + 2*self._columns + -2] = True
                    if not self.column(x) == self._columns:
                        knight_psuedo_attacks[x + 2*self._columns] = True
            if not self.row(x) == self._rows:
                if self.column(x) > 2:
                    knight_psuedo_attacks[x - self._columns - 3] = True
                if self.column(x) < (self._columns - 1):
                    knight_psuedo_attacks[x - self._columns + 1] = True
                if not self.row(x) == (self._rows -1):
                    if not self.column(x) == 1:
                        knight_psuedo_attacks[x - 2 * self._columns + -2] = True
                    if not self.column(x) == self._columns:
                        knight_psuedo_attacks[x - 2 * self._columns] = True
            self._rules[(Rules.PSEUDO_ATTACKS, Piece.KNIGHT, x)] = knight_psuedo_attacks.copy()

    def _generate_rook_pseudo_attacks(self):
        pass

    def _generate_bishop_pseudo_attacks(self):
        pass

    def _generate_queen_pseudo_attacks(self):
        pass

    def _generate_king_pseudo_attacks(self):
        king_psuedo_attacks = ebs(self._num_of_spaces)

        for x in range(1, self._num_of_spaces + 1):
            king_psuedo_attacks.setall(0)

            if not self.row(x) == 1:
                king_psuedo_attacks[x + self._columns -1] = True
                if not self.column(x) == 1:
                    king_psuedo_attacks[x + self._columns - 2] = True
                    king_psuedo_attacks[x - 2] = True
                if not self.column(x) == self._columns:
                    king_psuedo_attacks[x + self._columns] = True
                    king_psuedo_attacks[x] = True
            if not self.row(x) == self._rows:
                king_psuedo_attacks[x - self._columns - 1] = True
                if not self.column(x) == 1:
                    king_psuedo_attacks[x - self._columns - 2] = True
                if not self.column(x) == self._columns:
                    king_psuedo_attacks[x - self._columns] = True
            if not self.column(x) == 1:
                king_psuedo_attacks[x - 2] = True
            if not self.column(x) == self._columns:
                king_psuedo_attacks[x] = True
            self._rules[(Rules.PSEUDO_ATTACKS, Piece.KING, x)] = king_psuedo_attacks.copy()

@unique
class Piece(Enum):
    BISHOP = auto()
    KING = auto()
    KNIGHT = auto()
    ROOK = auto()
    PAWN = auto()
    QUEEN = auto()

@unique
class Rules(Enum):
    PSEUDO_ATTACKS = auto()

board = Chessboard()

board.add_piece(1, Piece.KING)
board.add_piece(6, Piece.PAWN)
board.add_piece(7, Piece.KNIGHT)

print(board.is_valid_attack(7,6))


#for k,v in board._rules.items():
#    print (k[1].name, k[2], v)
