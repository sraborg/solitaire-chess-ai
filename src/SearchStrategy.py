import abc


class SearchStrategy(abc.ABC):
    @abc.abstractmethod
    def search(self):
        pass


class DepthFirstSearch(SearchStrategy):
    def search(self):
        print("DFS Search Called")
        pass


class BreadthFirstSearch(SearchStrategy):
    def search(self):
        print("BFS Search Called")
        pass


x = DepthFirstSearch()

