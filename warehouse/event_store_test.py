from datetime import datetime
from unittest import TestCase
import unittest
from fake_bus import FakeBus
from warehouse.event_store import EventStore
from warehouse.events.product_received import ProductReceived
from warehouse.events.product_shipped import ProductShipped

class EventStoreTest(TestCase):

    __sut: EventStore

    def setUp(self) -> None:
        event_publisher = FakeBus()
        self.__sut = EventStore(event_publisher)
    
    @property
    def sut(self):
        return self.__sut

    def test_saves_event(self):
        event1 = ProductReceived('test_aggregate', 3, datetime.utcnow())
        event2 = ProductShipped('test_aggregate', 2, datetime.utcnow())

        self.sut.save_events('test_aggregate', [event1, event2])

        events = self.sut.get_events_for_aggregate('test_aggregate')
        self.assertEqual(2, len(events))
        self.assertEqual('ProductReceived', events[0].event_type)