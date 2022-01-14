from datetime import datetime
import unittest
from warehouse.events.product_received import ProductReceived
from warehouse.product import Product

class ProductTest(unittest.TestCase):

    def setUp(self):
        self.product = Product('a')
    
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
    
    def test_ship_with_enought_quantity_on_hand_succeedes(self):
        self.product.receive(1)
        result = self.product.ship(1)

        self.assertTrue(result.success)
    
    def test_ship_without_enough_quantity_on_hand_fails(self):
        self.product.receive(1)
        result = self.product.ship(2)

        self.assertFalse(result.success)

    def test_receive_rises_event(self):
        self.product.receive(5)

        self.assertEqual(1, len(self.product.changes))
        event = self.product.changes[0]
        self.assertEqual('ProductReceived', event.event_type)
        self.assertEqual(self.product.sku, event.sku)
        self.assertIsNotNone(event.timestamp)
        self.assertEqual(5, event.quantity)  

    def test_adjust_inventory_rises_event(self):
        self.product.adjust_inventory(6, 'magically found')

        self.assertEqual(1, len(self.product.changes))
        event = self.product.changes[0]
        self.assertEqual('InventoryAdjusted', event.event_type)
        self.assertEqual(self.product.sku, event.sku)
        self.assertIsNotNone(event.timestamp)
        self.assertEqual(6, event.quantity)
        self.assertEqual('magically found', event.reason)

    def test_ship_with_enough_quantity_on_hand_rises_event(self):
        self.product.load([ProductReceived('a', 7, datetime.utcnow())])
        self.product.ship(7)

        self.assertEqual(1, len(self.product.changes))
        event = self.product.changes[0]
        self.assertEqual('ProductShipped', event.event_type)
        self.assertEqual(self.product.sku, event.sku)
        self.assertIsNotNone(event.timestamp)
        self.assertEqual(7, event.quantity)

    def test_ship_without_enough_quantity_on_hand_doesnt_rise_event(self):
        self.product.load([ProductReceived('a', 6, datetime.utcnow())])
        self.product.ship(7)

        self.assertEqual(0, len(self.product.changes))