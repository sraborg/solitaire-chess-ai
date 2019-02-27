import abc
import copy


class SearchStrategy(abc.ABC):

    def __init__(self):
        self.solutionfound = False
        self.depth = 0
        self.expanded = 0
    @abc.abstractmethod
    def search(self, board, depth=0, *args, **kargs):
        pass


class DepthFirstSearch(SearchStrategy):

    def __init__(self):
        super(DepthFirstSearch, self).__init__()
        self.name = "Depth First Search"\

    def search(self, board_, depth=0, *args, **kargs):
        solutions = []

        expanded_ = 0
        # DFS Structures
        stack = []
        stack.append((board_, [], 0))

        while stack:
            board, move_sequence_, depth = stack.pop()
            pieces = board.num_of_pieces()

            # Check For Win Condition
            # Possible Solution Found
            if pieces < 2 and depth:

                # Save Depth
                if not solutions:
                    self.depth = depth
                    self.expanded = expanded_

                    if kargs.get("Full Search") is True:
                        break
                solutions.append((self.depth, self.expanded, move_sequence_))

            # Make Sure "max_iterations" Condition is met
            if kargs.get("max_iterations") is not None and depth >= kargs.get("max_iterations"):
                self.depth = depth
                self.expanded = expanded_
                break

            expanded_ = expanded_ + 1

            if kargs.get("max_iterations") is None or depth <= kargs.get("max_iterations"):

                # Queue Up Remaining
                attack_positions = board.legal_attack_positions()
                for position in attack_positions:  # Not Empty
                    attacker = board.position(position)
                    attacks = board.valid_attacks(position)

                    possible_attacks = []
                    for target_position in attacks:
                        move_sequence = move_sequence_.copy()
                        next_board = copy.deepcopy(board)
                        next_board.capture(position, target_position)
                        move = (attacker, position, target_position)
                        move_sequence.append(move)

                        stack.append((next_board, move_sequence, depth + 1))
        return solutions


class BreadthFirstSearch(SearchStrategy):

    def __init__(self):
        super(BreadthFirstSearch, self).__init__()
        self.name = "Breadth First Search"

    def search(self, board_, depth=0, **kargs):

        solutions = []
        expanded_ = 0
        # BFS Structures
        queue = []
        queue.insert(0,(board_,[],0))

        while queue:
            board, move_sequence_, depth = queue.pop()
            pieces = board.num_of_pieces()

            if not solutions:

                # Check For Win Condition
                # Possible Solution Found
                if pieces < 2 and depth:
                    # Save Depth
                    if not solutions:
                        self.depth = depth
                        self.expanded = expanded_
                    solutions.append((self.depth, self.expanded, move_sequence_))

                    # Make Sure "max_iterations" Condition is met
                    if depth is kargs.get("max_iterations"):
                        self.depth = depth
                        self.expanded = expanded_
                        break

            expanded_ = expanded_ + 1
            # Queue Up Remaining
            attack_positions = board.legal_attack_positions()
            for position in attack_positions:  # Not Empty
                attacker = board.position(position)
                attacks = board.valid_attacks(position)

                possible_attacks = []
                for target_position in attacks:
                    move_sequence = move_sequence_.copy()
                    next_board = copy.deepcopy(board)
                    next_board.capture(position, target_position)
                    move = (attacker, position, target_position)
                    move_sequence.append(move)

                    queue.insert(0, (next_board, move_sequence, depth+1))
        return solutions

class IterativeDeepeningSearch(SearchStrategy):

    def __init__(self):
        super(IterativeDeepeningSearch, self).__init__()
        self._search_algorithm = DepthFirstSearch()
        self.name = "Iterative Deepening Search"

    def search(self, board_, *args, iterations=100, **kargs):
        solutions = []

        expanded_ = 0
        move_sequence = []
        for x in range(iterations):
            solutions = solutions + self._search_algorithm.search(board_, move_sequence, solutions, max_iterations=x)
            expanded_ = expanded_ + self._search_algorithm.expanded

            if solutions:
                self.depth = self._search_algorithm.depth
                self.expanded = expanded_
                solution = solutions[0][2]
                solutions[0] = (self.depth, self.expanded, solution)
                break
        return solutions
