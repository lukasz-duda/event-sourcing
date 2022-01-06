from typing import List
from warehouse.event import Event

class AggregateRoot:

    events : List[Event]
    uncommitted_events : List[Event]

    def __init__(self) -> None:
        self.events = []
        self.uncommitted_events = []

    def add_event(self, event: Event):
        self.uncommitted_events.append(event)