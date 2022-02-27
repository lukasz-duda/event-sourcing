from abc import abstractclassmethod
from typing import List
from warehouse.events import Event

class AggregateRoot:

    __changes : List[Event]

    def __init__(self) -> None:
        self.__changes = []
    
    def load(self, events: List[Event]) -> None:
        for e in events:
            self._apply(e)
    
    @abstractclassmethod
    def _apply(self, event: Event) -> None:
        pass

    def _add_event(self, event: Event) -> None:
        self.__changes.append(event)
        self._apply(event)
    
    @property
    def changes(self) -> List[Event]:
        return self.__changes