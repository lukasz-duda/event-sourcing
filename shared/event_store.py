from typing import Dict, List
from shared.bus import EventPublisher
from warehouse.events import Event

class EventStore:

    __publisher: EventPublisher
    __streams: Dict[str, List[Event]]

    def __init__(self, event_publisher: EventPublisher) -> None:
        self.__publisher =  event_publisher
        self.__streams = dict()
    
    def save_events(self, aggregate_id: str, events: List[Event], expected_version: int):
        if aggregate_id not in self.__streams:
            self.__streams[aggregate_id] = []

        event_stream = self.__streams[aggregate_id]

        length = len(event_stream)
        if length > 0 and event_stream[length - 1].version != expected_version:
            raise ConcurrencyException

        version = expected_version
        for event in events:
            version += 1
            event.version = version
            event_stream.append(event)
            self.__publisher.publish(event)
    
    def get_events_for_aggregate(self, aggregate_id: str) -> List[Event]:
        if aggregate_id in self.__streams:
            return self.__streams[aggregate_id]
        else:
            raise AggregateNotFoundException

class AggregateNotFoundException(Exception):
    pass

class ConcurrencyException(Exception):
    pass