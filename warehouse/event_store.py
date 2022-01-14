from typing import List
from bus import EventPublisher
from warehouse.events.event import Event


class EventStore:

    __publisher: EventPublisher

    def __init__(self, event_publisher: EventPublisher) -> None:
        self.__publisher =  event_publisher
    
    def save_events(self, id: str, events: List[Event]):
        for event in events:
            self.__publisher.publish(event)
