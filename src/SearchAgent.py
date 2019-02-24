import SearchStrategy as Search


class SearchAgent:

    def __init__(self):
        self._search_strategy = Search.DepthFirstSearch();

    @property
    def search_strategy(self):
        print("getter called")
        return self._search_strategy

    @search_strategy.setter
    def search_strategy(self, value):
        print("setter called")

        if isinstance(value, Search.SearchStrategy):
            self._search_strategy = value
        else:
            print("Invalid SearchAgent")

    def search(self):
        self.search_strategy.search()
