import abc
from collections import defaultdict

class SubjectInterface(abc.ABC):

    def __init__(self):
        self._events = defaultdict(dict)

    def register_observer(self, event, observer_, callback):
        self._event_observers(event)[observer_] = callback

    def unregister_observer(self, event, observer_):
        del self._event_observers(event)[observer_]

    def notify_observers(self, event, message=None):
        self._event_observers(event)
        for observer, callback in self._event_observers(event).items():
            callback(message)

    def _event_observers(self, event):
        return self._events[event]

