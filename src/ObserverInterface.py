import abc


class ObserverInterface(abc.ABC):

    @abc.abstractmethod
    def update_observer(self, subject_):
        pass

