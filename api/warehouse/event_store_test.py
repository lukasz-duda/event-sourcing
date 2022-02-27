from shared.fake_bus import FakeBus
from shared.event_store import EventStore
from events import ProductReceived, ProductRegistered
from datetime import datetime
from unittest import TestCase

class EventStoreTest(TestCase):

    __sut: EventStore

    def setUp(self) -> None:
        event_publisher = FakeBus()
        self.__sut = EventStore(event_publisher)
    
    @property
    def sut(self):
        return self.__sut

    def test_saves_new_stream_events(self):
        event1 = ProductRegistered('test_aggregate', datetime.utcnow())
        event2 = ProductReceived('test_aggregate', 2, datetime.utcnow())

        self.sut.save_events('test_aggregate', [event1, event2], -1)

        events = self.sut.get_events_for_aggregate('test_aggregate')
        self.assertEqual(2, len(events))
        self.assertEqual('ProductRegistered', events[0].event_type)
        self.assertIsNotNone(events[0].timestamp)
        self.assertEqual('ProductReceived', events[1].event_type)
        self.assertIsNotNone(events[1].timestamp)