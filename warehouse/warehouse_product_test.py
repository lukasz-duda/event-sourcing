import unittest

from warehouse.warehouse_product import WarehouseProduct

class WarehouseProductTest(unittest.TestCase):

    def setUp(self):
        self.product = WarehouseProduct('a')
    
    def test_receive_increases_quantity(self):
        self.product.receive(1)
        
        self.assertEqual(1, self.product.quantityOnHand)
    
    def test_adjust_inventory_increases_quantity(self):
        self.product.adjust_inventory(1, 'found')
        
        self.assertEqual(1, self.product.quantityOnHand)
    
    def test_ship_decreases_quantity(self):
        self.product.receive(3)
        self.product.ship(1)
        
        self.assertEqual(2, self.product.quantityOnHand)

    def test_quantity_increases_quantity(self):
        self.product.receive(2)
        self.product.adjust_inventory(3, 'found')
        self.product.ship(1)
        
        self.assertEqual(4, self.product.quantityOnHand)
    
    def test_ship_succeedes_when_enough_quantity(self):
        self.product.receive(1)
        result = self.product.ship(1)

        self.assertTrue(result.success)
    
    def test_ship_fails_when_not_enough_quantity(self):
        self.product.receive(1)
        result = self.product.ship(2)

        self.assertFalse(result.success)

    def test_receive_rises_event(self):
        self.product.receive(1)

        self.assertEqual(1, len(self.product.uncommitted_events))
        event = self.product.uncommitted_events[0]
        self.assertEqual('ProductReceived', event.event_type)
        self.assertEqual(self.product.sku, event.sku)
        self.assertIsNotNone(event.timestamp)
        self.assertEqual(1, event.quantity)