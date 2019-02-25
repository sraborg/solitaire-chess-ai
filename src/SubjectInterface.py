import abc


class SubjectInterface(abc.ABC):

    @abc.abstractmethod
    def register_observer(self, observer_):
        pass

    @abc.abstractmethod
    def unregister_observer(self, observer_):
        pass

    @abc.abstractmethod
    def notify_observers(self):
        pass

