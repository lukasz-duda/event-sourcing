import requests
from typing import List
from shared.bus import EventPublisher
from warehouse.events import Event

class EventStoreDB:

    __publisher: EventPublisher

    def __init__(self, event_publisher: EventPublisher) -> None:
        self.__publisher =  event_publisher
    
    def save_events(self, aggregate_id: str, events: List[Event]):
        events_json = '[' + ', '.join(list(map(lambda event: event.to_json(), events))) + ']'
        headers = {'Content-Type': 'application/vnd.eventstore.events+json'}
        request_url = 'http://localhost:2113/streams/' + aggregate_id
        response = requests.post(request_url, data=events_json, headers=headers)

        for event in events:
            self.__publisher.publish(event)
    
    def get_events_for_aggregate(self, aggregate_id: str):
        headers = {'Accept': 'application/vnd.eventstore.events+json'}
        request_url = 'http://localhost:2113/streams/' + aggregate_id
        response = requests.get(request_url, headers=headers)
        return []