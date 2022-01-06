from typing import List
from warehouse.event import Event

class AggregateRoot:

    events : List[Event] = []
    uncommitted_events : List[Event] = []