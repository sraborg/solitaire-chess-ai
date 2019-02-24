from bitarray import bitarray
from enum import Enum, unique, auto
import math
from ExtendedBitArray import ExtendedBitArray as ebs


class Chessboard:

    _rules = {}

    def __init__(self, rows=3, columns=3):
        self._rows = rows
        self._columns = columns
        self._name = str(self._rows) + "x" + str(self._columns)
        self._num_of_spaces = rows * columns
        self._board = ebs(self._num_of_spaces)
        self._board.setall(0)

        self._location = {}
        #Chessboard._rules = {}

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

            index = (self._name, Rules.PSEUDO_ATTACKS, source_piece, source_location)
            attack_board = Chessboard._rules[index]
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
        if not Chessboard._rules.get(self._name):
            self._generate_pawn_pseudo_attacks()
            self._generate_knight_pseudo_attacks()
            self._generate_rook_pseudo_attacks()
            self._generate_bishop_pseudo_attacks()
            self._generate_queen_pseudo_attacks()
            self._generate_king_pseudo_attacks()
        Chessboard._rules[self._name] = True

    def _generate_pawn_pseudo_attacks(self):
        pawn_psuedo_attacks = ebs(self._num_of_spaces)

        for x in range(1, self._num_of_spaces + 1):
            pawn_psuedo_attacks.setall(0)

            if self.row(x) == 1:
                Chessboard._rules[(self._name, Rules.PSEUDO_ATTACKS, Piece.PAWN, x)] = pawn_psuedo_attacks
            else:
                if not self.column(x) == 1:
                    pawn_psuedo_attacks[x + self._columns - 2] = True
                if not self.column(x) == self._columns:
                    pawn_psuedo_attacks[x + self._columns ] = True
                    pass
                Chessboard._rules[(self._name, Rules.PSEUDO_ATTACKS, Piece.PAWN, x)] = pawn_psuedo_attacks.copy()

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
            Chessboard._rules[(self._name, Rules.PSEUDO_ATTACKS, Piece.KNIGHT, x)] = knight_psuedo_attacks.copy()

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
            Chessboard._rules[(self._name, Rules.PSEUDO_ATTACKS, Piece.KING, x)] = king_psuedo_attacks.copy()

    def rank(self, position):
            if self._valid_board_space(position):
                index = position - 1
                rank_mask = ebs(self._num_of_spaces)
                rank_mask.setall(0)

                while rank_mask[index] == False:
                    rank_mask[index] = True
                    index = (index + self._columns) % self._num_of_spaces
                return rank_mask

    def file(self, position):
        try:
            if position < 1 or position > self._num_of_spaces:
                raise ValueError("Invalid Position")
            else:
                index = position - 1
                row = math.floor(index / self._columns)
                rank_mask = ebs(self._num_of_spaces)
                rank_mask.setall(0)
                start = row * self._columns
                for i in range(self._columns):
                    rank_mask[start + i] = True
                    index = (index + 1) % self._num_of_spaces
                return rank_mask
        except ValueError:
            raise

    def diagonal(self, position):
        if self._valid_board_space(position):
            index = position - 1
            diagonal_mask = ebs(self._num_of_spaces)
            diagonal_mask.setall(0)
            starting_column = self.column(position)

            # Mark NE
            while index < self._num_of_spaces and starting_column <= self.column(index + 1):
                diagonal_mask[index] = True
                index = (index + self._columns) + 1

            '''
            # Mark SW
            index = position - 2 - self._columns
            while index >= 0 and starting_column >= self.column(index + 1):
                diagonal_mask[index] = True
                index = (index - self._columns) - 1
            '''
            return diagonal_mask
        pass

    def anti_diagonal(self,position):
        if self._valid_board_space(position):
            index = position - 1
            antidiagonal_mask = ebs(self._num_of_spaces)
            antidiagonal_mask.setall(0)
            starting_column = self.column(position)

            antidiagonal_mask[index] = True
            # Mark SE
            index = position - self._columns
            while index >= 0 and starting_column < self.column(index + 1):
                antidiagonal_mask[index] = True
                index = (index - self._columns) + 1


            # Mark NW
            index = position + self._columns - 2
            while index < self._num_of_spaces and starting_column > self.column(index + 1):
                antidiagonal_mask[index] = True
                index = (index + self._columns) - 1

            return antidiagonal_mask

    def _get_ray_attack(self, position, ray):
        try:
            if not isinstance(ray, Rays):
                raise ValueError("Invalid Ray")
            if self._valid_board_space(position):

                is_flipped = False  # Flagged Used to re-flip board if needed

                occupancy = self._board.copy()

                # Used for Negative Rays Attacks
                # Instead of changing calculations,
                # The board is just flipped with index/positions/rays reset accordingly
                if not Rays.is_positive(ray):
                    occupancy.reverse()
                    if ray is Rays.WEST:
                        ray = Rays.EAST
                    elif ray is Rays.SOUTH_WEST:
                        ray = Rays.NORTH_EAST
                    elif ray is Rays.SOUTH:
                        ray = Rays.NORTH
                    elif ray is Rays.SOUTH_EAST:
                        ray = Rays.NORTH_WEST

                    position = self._num_of_spaces - position + 1
                    is_flipped = True

                index = position - 1
                occupancy_reversed = occupancy.copy()
                occupancy_reversed.reverse()

                mask = ebs(self._num_of_spaces)
                mask.setall(0)

                # Check North & South
                if ray is Rays.NORTH or ray is Rays.SOUTH:
                    rank_mask = self.rank(position)
                    mask = mask | rank_mask

                # Check East & West
                elif ray is Rays.EAST or ray is Rays.WEST:
                    file_mask = self.file(position)
                    mask = mask | file_mask

                # Check NE & SW
                elif ray is Rays.NORTH_EAST or ray is Rays.SOUTH_WEST:
                    diagonal_mask = self.diagonal(position)
                    mask = mask | diagonal_mask

                # NW & SE
                else:
                    anti_diagonal_mask = self.anti_diagonal(position)
                    mask = mask | anti_diagonal_mask

                potential_blockers = occupancy & mask
                slider_position = ebs(self._num_of_spaces)
                slider_position.setall(False)
                slider_position[index] = True



                shifted_slider_position = (slider_position.copy() >> 1)
                # Calculations // Everything is reversed to do math
                potential_blockers.reverse()
                shifted_slider_position.reverse()

                changes = (potential_blockers - shifted_slider_position)
                changes.resize(self._num_of_spaces)
                changes = (occupancy_reversed ^ changes)
                changes.reverse()
                attacks = changes & mask & occupancy
                attacks[index] = False

                if is_flipped:
                    attacks.reverse()
                return attacks
        except ValueError:
            raise

    def _get_negative_ray_attack(self,position):
        pass

@unique
class Piece(Enum):
    BISHOP = auto()
    KING = auto()
    KNIGHT = auto()
    ROOK = auto()
    PAWN = auto()
    QUEEN = auto()

    @staticmethod
    def is_sliding_piece(piece):
        try:
            if not isinstance(piece, Piece):
                raise ValueError("Invalid Piece")
            if piece is Piece.QUEEN or piece is Piece.BISHOP or piece is Piece.ROOK:
                return True
            else:
                return False
        except ValueError:
            raise
@unique
class Rules(Enum):
    PSEUDO_ATTACKS = auto()

@unique
class Rays(Enum):
    NORTH = auto()
    NORTH_EAST = auto()
    EAST = auto()
    SOUTH_EAST = auto()
    SOUTH = auto()
    SOUTH_WEST = auto()
    WEST = auto()
    NORTH_WEST = auto()

    @staticmethod
    def is_positive(ray):
        try:
            if not isinstance(ray, Rays):
                raise ValueError("Invalid Ray")

            if ray in [Rays.NORTH, Rays.NORTH_EAST, Rays.NORTH_WEST, Rays.EAST]:
                return True
            else:
                return False
        except:
            raise



board = Chessboard(rows=4, columns=4)
board.add_piece(1, Piece.BISHOP)
board.add_piece(5, Piece.ROOK)
board.add_piece(6, Piece.QUEEN)
board.add_piece(7, Piece.PAWN)
board.add_piece(8, Piece.PAWN)
board.add_piece(9, Piece.PAWN)
board.add_piece(11, Piece.KNIGHT)
board.add_piece(13, Piece.PAWN)
board.add_piece(16, Piece.BISHOP)
board.print_board()
print("-------")

att = Chessboard(rows=4, columns=4)
att._board = board._get_ray_attack(11, Rays.SOUTH_WEST)
att.print_board()

print("-------")
