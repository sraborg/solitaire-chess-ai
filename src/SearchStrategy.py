import abc
import copy


class SearchStrategy(abc.ABC):
    @abc.abstractmethod
    def search(self, board, *args, **kargs):
        pass


class DepthFirstSearch(SearchStrategy):

    def search(self, board_, *args, **kargs):
        possible_solutions = []
        move_sequence = []
        max_iterations_ = kargs.get("max_iterations")
        self._search(board_, move_sequence, possible_solutions, 0, max_iterations=max_iterations_)
        return possible_solutions

    def _search(self, board_, move_sequence_, possible_solutions_, depth, **kargs):

        pieces = board_.num_of_pieces()

        # Exit if a solution is found unless "complete_search" flag is set
        if possible_solutions_ and not kargs.get("complete_search"):
            return

        # Base Case
        # Possible Solution Found
        if pieces < 2:
            possible_solutions_.append(move_sequence_)
            return
        elif depth is kargs.get("max_iterations"):                   # Exit if "max_iterations" is set and reached
            return
        else:
            attack_positions = board_.legal_attack_positions()

            for position in attack_positions:                        # Not Empty
                attacker = board_.position(position)
                attacks = board_.valid_attacks(position)

                for target_position in attacks:
                    move_sequence = move_sequence_.copy()
                    board = copy.deepcopy(board_)
                    board.capture(position, target_position)
                    move = (attacker, position, target_position)
                    move_sequence.append(move)
                    self._search(board, move_sequence, possible_solutions_, depth+1, max_iterations=kargs.get("max_iterations"))


class BreadthFirstSearch(SearchStrategy):

    def search(self, board_, *args, **kargs):
        print("===================")
        print("BFS CALLED")
        print("===================")
        possible_solutions = []
        move_sequence = []
        self._search(board_, move_sequence, possible_solutions, 0)
        return possible_solutions

    def _search(self, board_, move_sequence_, possible_solutions_, depth):
        print("DEPTH: ", depth)
        pieces = board_.num_of_pieces()

        # Base Case
        # Possible Solution Found
        if pieces < 2:
            # print("DEPTH: ", depth)
            possible_solutions_.append(move_sequence_)
            return
        else:
            attack_positions = board_.legal_attack_positions()

            for position in attack_positions:  # Not Empty
                attacker = board_.position(position)
                attacks = board_.valid_attacks(position)

                possible_attacks = []
                for target_position in attacks:
                    move_sequence = move_sequence_.copy()
                    board = copy.deepcopy(board_)
                    # print("=====================")
                    # print("DEPTH: ", depth)
                    # board.print_board()
                    board.capture(position, target_position)
                    # print("-------------------")
                    move = (attacker, position, target_position)
                    move_sequence.append(move)
                    # print("Move: ", move)
                    # print("Move Sequence: ", move_sequence)
                    # board.print_board()
                    # print("=====================")
                    transition = (board, move_sequence)
                    possible_attacks.append(transition)

                for k,v in possible_attacks:
                    self._search(k, v, possible_solutions_, depth + 1)


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
