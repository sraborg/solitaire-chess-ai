from bitarray import bitarray
from enum import Enum, unique, auto
from SubjectInterface import *
import math
import copy

from ExtendedBitArray import ExtendedBitArray as ebs


class Chessboard(SubjectInterface):

    _rules = {}

    def __init__(self, rows=4, columns=4):
        super(Chessboard, self).__init__()
        self._observers = {}
        #self._events[BoardEvent.CHANGE] = {}

        self._rows = rows
        self._columns = columns
        self._name = str(self._rows) + "x" + str(self._columns)
        self._num_of_spaces = rows * columns
        self._board = ebs(self._num_of_spaces)
        self._board.setall(0)

        self._location = {}         # Stores Pieces by Index (not by Position)
        self._position = {}
        #Chessboard._rules = {}

        self._generate_psuedo_attacks()

    ##
    #   Adds a Chesspiece to the board
    #
    #   @param position The position to put the piece
    #   @param The chess piece

    def add_piece(self, position, piece):
        try:
            if not self._valid_board_space(position):
                raise ValueError("Invalid Location")

            elif not isinstance(piece, Piece):
                raise ValueError("Invalid Piece")

            else:
                index = position - 1
                self._board[index] = True
                self._position[position] = piece
                self.notify_observers(BoardEvent.CHANGE,BoardEvent.CHANGE)

        except ValueError:
            raise

    ##
    #   Removes a Chesspiece to the board
    #
    #   @param position The position of the piece
    #   @param The chess piece
    def remove_piece(self, position):
        index = position-1
        self._position[position] = None
        self._location[index] = None
        self._board[index] = False
        self.notify_observers(BoardEvent.CHANGE, BoardEvent.CHANGE)

    ##
    #   Performs a capture move
    #
    #   Verifies move is legal. If so, attacker takes the place of target piece
    #   @param source_position The attackers position
    #   @param target_position The target position

    def capture(self, source_position, target_position):
        if self.is_valid_attack(source_position, target_position):

            self.remove_piece(target_position)
            attacker = self._position.get(source_position)
            self.add_piece(target_position, attacker)

            self.remove_piece(source_position)

    ##
    #   Determines which board positions can make legal attacks
    #
    #   @return List of Positions

    def legal_attack_positions(self):
        attack_positions = []
        for index in range(self._num_of_spaces):
            position = index + 1
            if self._position.get(position) is not None:
                legal_attacks = self._valid_attacks(position)
                if legal_attacks.count() > 0:
                    attack_positions.append(position)
        return attack_positions

    ##
    #   Counts the number of pieces on the board
    #
    #   @return Number of pieces
    def num_of_pieces(self):
        return self._board.count()

    ##
    #   Checks if a piece can attack another
    #
    #   @param source_position The position of the attacker
    #   @param target_position The position of the target
    #
    #   @return True/False
    #
    def is_valid_attack(self, source_position, target_position):
        try:
            target_index = target_position - 1
            attacker = self._position.get(source_position)
            if attacker == None:
                raise ValueError("Invalid Source Location: " + str(source_position))

            victim = self._position.get(target_position)
            if victim == None:
                raise ValueError("Invalid Target Location" + str(target_position))

            if Piece.is_sliding_piece(attacker):
                attack_board = self._valid_sliding_piece_attacks(source_position)

            else:
                #index = (self._name, Rules.PSEUDO_ATTACKS, attacker, source_position)
                attack_board = self._valid_non_sliding_piece_attacks(source_position)  #Chessboard._rules[index]
            test_board = attack_board & self._board
            return test_board[target_index]
        except ValueError:
            raise

    ##
    #   Prints crude board representation
    def print_board(self):
        board_string = self._board.to01()[::-1]

        for x in range(0, self._rows):
            start = x * self._columns
            end = start + self._columns
            row_string = slice(start, end)
            print(board_string[row_string][::-1])

    ##
    #
    def print_pieces(self):
        for k,v in self._location.items():
            print(v.name, "at position", k)

    ##
    #   Determines all piece positions
    #
    #   @return List of all pieces and their associated board position
    def pieces(self):
        pieces_list = []
        for k, v in self._position.items():
            pieces_list.append((k, v))
        return pieces_list

    ##
    #   Checks what piece is at a board position
    #
    #   @param position Board position to check
    #   @param Return Chess Piece or None
    def position(self, position):
        return self._position.get(position)

    ##
    #   Determines what row a board position is in
    #
    #   @param position Board position
    #   @return the row number
    def row(self, position):
        try:
            if not self._valid_board_space(position):
                raise ValueError("Invalid Location")
            else:
                index = self._num_of_spaces - (position -1)
                return math.ceil(index / self._columns)
        except ValueError:
            raise

    ##
    #   Determines what column a board position is in
    #
    #   @param position Board position
    #   @return the row number
    def column(self, position):
        try:
            if not self._valid_board_space(position):
                raise ValueError("Invalid Location")
            else:
                return ((position-1) % self._columns) +1
        except ValueError:
            raise

    ##
    #   Verifies a position is actually on the board
    #
    #   @param position Position to check
    #   @return True/False

    def _valid_board_space(self, position):
        if position > 0 and position <= self._num_of_spaces:
            return True
        else:
            return False

    ##
    #   Caches legal pseudo-attacks at every board position
    #   for Pawns, Kings, and Knights
    def _generate_psuedo_attacks(self):
        if not Chessboard._rules.get(self._name):
            self._generate_pawn_pseudo_attacks()
            self._generate_knight_pseudo_attacks()
            self._generate_king_pseudo_attacks()
        Chessboard._rules[self._name] = True


    ##
    #   Determines all legal pseudo-attacks for pawns at
    #   every board position
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

    ##
    #   Determines all legal pseudo-attacks for knights at
    #   every board position
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

    ##
    #   Determines all legal pseudo-attacks for Kings at
    #   every board position
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

    ##
    #   @return List of Positions
    def valid_attacks(self, position):
        attacks = []
        try:
            board = self._board.copy()
            board = self._valid_attacks(position)
            while True:
                # Loop through EBS and find first True
                index = board.index(True)  # Will Raise ValueError when all Zeros
                board[index] = False
                position = index + 1
                attacks.append(position)

        except ValueError as e:  # No More attacks
            return attacks
            pass
    ##
    #   Determines a positions legal attacks.
    #
    #   Wrapper for _valid_sliding_piece_attacks() & _valid_non_sliding_piece_attacks()
    #
    #   @param position Board position
    #   @returns EBS Board indicating legal attacks
    def _valid_attacks(self, position):
        # Validation done in child method calls
        attacker =  self._position.get(position)

        if Piece.is_sliding_piece(attacker):
            return self._valid_sliding_piece_attacks(position)
        else:
            return self._valid_non_sliding_piece_attacks(position)

    ##
    #   Determines legal attacks for Bishops, Queens, and Rooks
    #
    #   @param position Board position
    #   @returns EBS Board indicating legal attacks
    def _valid_sliding_piece_attacks(self, position):
        try:
            attacker = self._position.get(position)

            if not Piece.is_sliding_piece(attacker):
                raise ValueError("Invalid Piece. Piece must be a slider")
            if self._valid_board_space(position):
                attack_board = ebs(self._num_of_spaces)
                attack_board.setall(False)
                if attacker in {Piece.ROOK, Piece.QUEEN}:
                    north_attacks = self._board & self._get_ray_attack(position, Rays.NORTH)
                    east_attacks = self._board & self._get_ray_attack(position, Rays.EAST)
                    south_attacks = self._board & self._get_ray_attack(position, Rays.SOUTH)
                    west_attacks = self._board & self._get_ray_attack(position, Rays.WEST)
                    attack_board = north_attacks | east_attacks | south_attacks | west_attacks
                if attacker in {Piece.BISHOP, Piece.QUEEN}:
                    ne_attacks = self._board & self._get_ray_attack(position, Rays.NORTH_EAST)
                    se_attacks = self._board & self._get_ray_attack(position, Rays.SOUTH_EAST)
                    sw_attacks = self._board & self._get_ray_attack(position, Rays.SOUTH_WEST)
                    nw_attacks = self._board & self._get_ray_attack(position, Rays.NORTH_WEST)
                    attack_board = attack_board | ne_attacks | se_attacks | sw_attacks | nw_attacks
                return attack_board
        except:
            raise

    ##
    #   Determines legal attacks for Kings, Knights, and Pawns
    #
    #   @param position Board position
    #   @returns EBS Board indicating legal attacks
    def _valid_non_sliding_piece_attacks(self, position):
        try:
            if self._valid_board_space(position):

                attacker = self._position.get(position)

                if attacker == None:
                    raise ValueError("Invalid Source Location. Empty Board Space")

                index = (self._name, Rules.PSEUDO_ATTACKS, attacker, position)
                return Chessboard._rules[index] & self._board
        except ValueError:
            raise

    ##
    #   Finds the rank (column) of a given position
    #
    #   @param position Board Position
    #   @return EBS Board indicating rank
    def rank(self, position):
            if self._valid_board_space(position):

                # Check For Cached Answer
                if self._rules.get((self._name, Rules.RANK, position)):
                    return self._rules.get((self._name, Rules.RANK, position))

                index = position - 1
                rank_mask = ebs(self._num_of_spaces)
                rank_mask.setall(0)

                while rank_mask[index] == False:
                    rank_mask[index] = True
                    index = (index + self._columns) % self._num_of_spaces

                self._rules[(self._name, Rules.RANK, position)] = rank_mask       # Cache Result
                return rank_mask

    ##
    #   Finds the file (row) of a given position
    #
    #   @param position Board Position
    #   @return EBS Board indicating file
    def file(self, position):
        if self._valid_board_space(position):

            # Check For Cached Answer
            if self._rules.get((self._name, Rules.FILE, position)):
                return self._rules.get((self._name, Rules.FILE, position))

            index = position - 1
            row = math.floor(index / self._columns)
            file_mask = ebs(self._num_of_spaces)
            file_mask.setall(0)
            start = row * self._columns
            for i in range(self._columns):
                file_mask[start + i] = True
                index = (index + 1) % self._num_of_spaces

            self._rules[(self._name, Rules.FILE, position)] = file_mask  # Cache Result
            return file_mask

    ##
    #   Finds the diagonal of a given position
    #
    #   @param position Board Position
    #   @return EBS Board indicating diagonal
    def diagonal(self, position):
        if self._valid_board_space(position):

            # Check For Cached Answer
            if self._rules.get((self._name, Rules.DIAGONAL, position)):
                return self._rules.get((self._name, Rules.DIAGONAL, position))

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

            self._rules[(self._name, Rules.DIAGONAL, position)] = diagonal_mask  # Cache Result
            return diagonal_mask
        pass

    ##
    #   Finds the anti-diagonal of a given position
    #
    #   @param position Board Position
    #   @return EBS Board indicating anti-diagonal
    def anti_diagonal(self,position):
        if self._valid_board_space(position):

            # Check For Cached Answer
            if self._rules.get((self._name, Rules.ANTI_DIAGONAL, position)):
                return self._rules.get((self._name, Rules.ANTI_DIAGONAL, position))

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

                self._rules[(self._name, Rules.ANTI_DIAGONAL, position)] = antidiagonal_mask  # Cache Result
            return antidiagonal_mask

    ##
    #   Determines legal attacks on a given ray
    #
    #   @param position Board Position
    #   @param ray The cardinal direction to check
    #   @return EBS Board indicating diagonal
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

                # Check North
                if ray is Rays.NORTH:
                    rank_mask = self.rank(position)
                    mask = mask | rank_mask

                # Check East
                elif ray is Rays.EAST:

                    # Fixes a glitch when checking EAST attacks while in last column
                    if position % self._rows is 0:
                        no_attacks = ebs(self._num_of_spaces)
                        no_attacks.setall(0)
                        return ebs(no_attacks)


                    file_mask = self.file(position)
                    mask = mask | file_mask

                # Check NE
                elif ray is Rays.NORTH_EAST:
                    diagonal_mask = self.diagonal(position)
                    mask = mask | diagonal_mask

                # Check NW
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


    # Implement Subject Interface Methods

    def __deepcopy__(self, memodict={}):
        nb = Chessboard(self._rows, self._columns)
        nb._board = copy.deepcopy(self._board)
        nb._position = copy.deepcopy(self._position)
        nb._generate_psuedo_attacks()
        return nb
@unique
class BoardEvent(Enum):
    CHANGE = auto()

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
    RANK = auto()
    FILE = auto()
    DIAGONAL = auto()
    ANTI_DIAGONAL = auto()

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


