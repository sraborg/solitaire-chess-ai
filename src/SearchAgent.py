from SearchStrategy import *
from Chessboard import Chessboard as cb
from Chessboard import Piece


class SearchAgent:

    def __init__(self):
        self._search_strategy = DepthFirstSearch();
        self._chessboard = None

    @property
    def chessboard(self):
        return self._chessboard

    @chessboard.setter
    def chessboard(self,value):
        try:
            if not isinstance(value, cb):
                raise ValueError("Invalid Chessboard")

            self._chessboard = value
        except ValueError:
            raise
    @property
    def search_strategy(self):
        return self._search_strategy

    @search_strategy.setter
    def search_strategy(self, value):
        try:
            if not isinstance(value, Search.SearchStrategy):
                raise ValueError("Invalid Search Agent")

            self._search_strategy = value
        except ValueError:
            raise

    def search(self):
        try:
            if not isinstance(self.search_strategy, SearchStrategy):
                raise Exception("No Search Strategy Set")
            if not isinstance(self.chessboard, cb):
                raise Exception("No Chessboard Set")

            gamestate = self.chessboard
            print(self.search_strategy.search(gamestate))
        except Exception as e:
            print(e)
            raise



board = cb()
board.add_piece(3, Piece.PAWN)
board.add_piece(6, Piece.KNIGHT)
board.add_piece(13, Piece.ROOK)
board.add_piece(15, Piece.QUEEN)
#board.print_board()
#print("-------")



position = 6
att = cb()
#att._board = board._valid_attacks(position)
#att.print_board()
#print(position, board.valid_attacks(position))

agent = SearchAgent()
agent.chessboard = board
agent.search()
#print("-------")
#board.capture(11,13)
#board.print_board()