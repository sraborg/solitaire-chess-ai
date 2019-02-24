import abc
import copy


class SearchStrategy(abc.ABC):
    @abc.abstractmethod
    def search(self, board, *args, **kargs):
        pass


class DepthFirstSearch(SearchStrategy):

    def search(self, board_, *args, **kargs):

        solutions = []

        # DFS Structures
        stack = []
        stack.append((board_, [], 0))

        while stack:
            board, move_sequence_, depth = stack.pop()
            pieces = board.num_of_pieces()

            # Check For Win Condition
            # Possible Solution Found
            if pieces < 2 and depth:
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

                    stack.append((next_board, move_sequence, depth + 1))
        return solutions


class BreadthFirstSearch(SearchStrategy):

    def search(self, board_, depth=0, **kargs):
        solutions = []

        # BFS Structures
        queue = []
        queue.insert(0,(board_,[],0))

        while queue:
            board, move_sequence_, depth = queue.pop()
            pieces = board.num_of_pieces()

            # Check For Win Condition
            # Possible Solution Found
            if pieces < 2 and depth:
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

    def search(self, board_, *args, iterations=8, **kargs):
        possible_solutions = []
        move_sequence = []
        for x in range(iterations):
            possible_solutions = possible_solutions + self._search_algorithm.search(board_, move_sequence, possible_solutions, 0, max_iterations=x)
            if possible_solutions:
                break
        return possible_solutions
