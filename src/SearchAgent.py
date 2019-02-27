from SearchStrategy import *
from SubjectInterface import *
from Chessboard import Chessboard as cb
from Chessboard import Piece
from enum import Enum, unique, auto


class SearchAgent(SubjectInterface):

    def __init__(self):
        super(SearchAgent, self).__init__()
        self.solutions = []
        self._search_strategy = DepthFirstSearch()
        self.algorithm = self._search_strategy.name
        self._chessboard = None
        self.results = None


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
            if not isinstance(value, SearchStrategy):
                raise ValueError("Invalid Search Agent")

            self._search_strategy = value
            self.algorithm = self._search_strategy.name

        except ValueError:
            raise

    def search(self):
        try:
            if not isinstance(self.search_strategy, SearchStrategy):
                raise Exception("No Search Strategy Set")
            if not isinstance(self.chessboard, cb):
                raise Exception("No Chessboard Set")

            gamestate = self.chessboard
            self.solutions = self.search_strategy.search(gamestate)
            #message = (self.search_strategy.name, self.search_strategy.depth, self.search_strategy.expanded, self.solutions)
            self.notify_observers(SearchAgentEvent.SEARCH_COMPLETE, SearchAgentEvent.SEARCH_COMPLETE)

        except Exception as e:
            print(e)
            raise

    def print_solution(self):
        print(self.solutions)

@unique
class SearchAgentEvent(Enum):
    SEARCH_COMPLETE = auto()


'''
# PUZZLE 1
board = cb()
board.add_piece(3, Piece.PAWN)
board.add_piece(6, Piece.KNIGHT)
board.add_piece(13, Piece.ROOK)
board.add_piece(15, Piece.QUEEN)


# PUZZLE 2
board2 = cb()
board2.add_piece(6, Piece.PAWN)
board2.add_piece(9, Piece.ROOK)
board2.add_piece(10, Piece.BISHOP)
board2.add_piece(14, Piece.ROOK)
board2.add_piece(15, Piece.PAWN)

# PUZZLE 3
board3 = cb()
board3.add_piece(3, Piece.ROOK)
board3.add_piece(7, Piece.PAWN)
board3.add_piece(9, Piece.ROOK)
board3.add_piece(10, Piece.KING)
board3.add_piece(11, Piece.QUEEN)
board3.add_piece(16, Piece.PAWN)

# PUZZLE 4
board4 = cb()
board4.add_piece(1, Piece.PAWN)
board4.add_piece(2, Piece.BISHOP)
board4.add_piece(3, Piece.PAWN)
board4.add_piece(6, Piece.ROOK)
board4.add_piece(9, Piece.BISHOP)
board4.add_piece(10, Piece.KING)
board4.add_piece(11, Piece.KNIGHT)
board4.add_piece(16, Piece.ROOK)


agent = SearchAgent()

print("=== PUZZLE 1 ===")


bfs = BreadthFirstSearch()
ids = IterativeDeepeningSearch()


board.print_board()
agent.chessboard = board

agent.search()
print(agent.solutions)
print("depth: ", agent.search_strategy.depth, "expanded: ", agent.search_strategy.expanded)


agent.search_strategy = bfs
agent.search()
print(agent.solutions)
print("depth: ", agent.search_strategy.depth, "expanded: ", agent.search_strategy.expanded)

agent.search_strategy = ids
agent.search()
print(agent.solutions)
print("depth: ", agent.search_strategy.depth, "expanded: ", agent.search_strategy.expanded)


board2.print_board()
agent.chessboard = board2
agent.search()
print(agent.solutions)
print("depth: ", agent.search_strategy.depth, "expanded: ", agent.search_strategy.expanded)

agent.search_strategy = bfs
agent.search()
print(agent.solutions)
print("depth: ", agent.search_strategy.depth, "expanded: ", agent.search_strategy.expanded)

agent.search_strategy = ids
agent.search()
print(agent.solutions)
print("depth: ", agent.search_strategy.depth, "expanded: ", agent.search_strategy.expanded)


board3.print_board()
agent.chessboard = board3
agent.search()
print(agent.solutions)
print("depth: ", agent.search_strategy.depth, "expanded: ", agent.search_strategy.expanded)


agent.search_strategy = bfs
agent.search()
print(agent.solutions)
print("depth: ", agent.search_strategy.depth, "expanded: ", agent.search_strategy.expanded)

agent.search_strategy = ids
agent.search()
print(agent.solutions)
print("depth: ", agent.search_strategy.depth, "expanded: ", agent.search_strategy.expanded)

board4.print_board()
agent.chessboard = board4
agent.search()
print(agent.solutions)
print("depth: ", agent.search_strategy.depth, "expanded: ", agent.search_strategy.expanded)


agent.search_strategy = bfs
agent.search()
print(agent.solutions)
print("depth: ", agent.search_strategy.depth, "expanded: ", agent.search_strategy.expanded)


agent.search_strategy = ids
agent.search()
print(agent.solutions)
print("depth: ", agent.search_strategy.depth, "expanded: ", agent.search_strategy.expanded)
'''

