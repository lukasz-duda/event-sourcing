from typing import List
from warehouse.event import Event

class AggregateRoot:

    _events : List[Event]
    _uncommitted_events : List[Event]

    def __init__(self) -> None:
        self._events = []
        self._uncommitted_events = []

    def add_event(self, event: Event):
        self._uncommitted_events.append(event)
    
    @property
    def uncommitted_events(self) -> List[Event]:
        return self._uncommitted_events