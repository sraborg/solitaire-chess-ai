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
        self._search(board_, move_sequence, possible_solutions, 0)
        return possible_solutions

    def _search(self, board_, move_sequence_, possible_solutions_, depth):


        pieces = board_.num_of_pieces()

        # Base Case
        # Possible Solution Found
        if pieces < 2:
            #print("DEPTH: ", depth)
            possible_solutions_.append(move_sequence_)
            return
        else:
            attack_positions = board_.legal_attack_positions()

            for position in attack_positions:                        # Not Empty
                attacker = board_.position(position)
                attacks = board_.valid_attacks(position)

                for target_position in attacks:
                    move_sequence = move_sequence_.copy()
                    board = copy.deepcopy(board_)
                    #print("=====================")
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
                    self._search(board, move_sequence, possible_solutions_, depth+1)

class BreadthFirstSearch(SearchStrategy):
    def search(self, board, *args, **kargs):
        print("BFS Search Called")
        pass


x = DepthFirstSearch()

