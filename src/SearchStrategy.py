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

    def search(self, board_, depth=0, *args, **kargs):
        solutions = []
        expanded_ = 0
        # DFS Structures
        stack = []
        stack.append((board_, [], 0))

        while stack:
            board, move_sequence_, depth = stack.pop()
            pieces = board.num_of_pieces()
            expanded_ = expanded_ + 1

            if not solutions:
                self.expanded = expanded_ + 1
            # Check For Win Condition
            # Possible Solution Found
            if pieces < 2 and depth:

                # Save Depth
                if not solutions:
                    self.depth = depth
                solutions.append(move_sequence_)

                # Make Sure "max_iterations" Condition is met
                if depth is kargs.get("max_iterations"):
                    break


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

    def search(self, board_, depth=0, **kargs):

        solutions = []
        expanded_ = 0
        # BFS Structures
        queue = []
        queue.insert(0,(board_,[],0))

        while queue:
            board, move_sequence_, depth = queue.pop()
            pieces = board.num_of_pieces()

            expanded_ = expanded_ + 1
            if not solutions:
                self.expanded = expanded_ + 1

            # Check For Win Condition
            # Possible Solution Found
            if pieces < 2 and depth:
                # Save Depth
                if not solutions:
                    self.depth = depth
                solutions.append(move_sequence_)

                # Make Sure "max_iterations" Condition is met
                if depth is kargs.get("max_iterations"):
                    break

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


    _search_algorithm = DepthFirstSearch()

    def search(self, board_, *args, iterations=100, **kargs):
        possible_solutions = []
        move_sequence = []
        for x in range(iterations):
            possible_solutions = possible_solutions + self._search_algorithm.search(board_, move_sequence, possible_solutions, max_iterations=x)
            self.expanded = self.expanded + self._search_algorithm.expanded

            if possible_solutions:
                self.depth = self._search_algorithm.depth
                break
        return possible_solutions
