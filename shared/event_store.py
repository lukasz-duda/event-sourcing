from typing import Dict, List
from shared.bus import EventPublisher
from warehouse.events import Event

class EventStore:

    __publisher: EventPublisher
    __streams: Dict[str, List[Event]]

    def __init__(self, event_publisher: EventPublisher) -> None:
        self.__publisher =  event_publisher
        self.__streams = dict()
    
    def save_events(self, aggregate_id: str, events: List[Event]):
        if aggregate_id in self.__streams:
            stream_events = self.__streams[aggregate_id]
            for new_event in events:
                stream_events.append(new_event)
        else:
            self.__streams[aggregate_id] = events

        for event in events:
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