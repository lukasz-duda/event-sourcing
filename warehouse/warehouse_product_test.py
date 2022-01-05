import unittest

from warehouse.warehouse_product import WarehouseProduct

class WarehouseProductTest(unittest.TestCase):

    def setUp(self):
        self.product = WarehouseProduct('a')
    
    def test_receive(self):
        self.product.receive(1)
        
        self.assertEqual(1, self.product.quantity)
    
    def test_adjust_inventory(self):
        self.product.adjust_inventory(1, 'found')
        
        self.assertEqual(1, self.product.quantity)
    
    def test_ship(self):
        self.product.receive(3)
        self.product.ship(1)
        
        self.assertEqual(2, self.product.quantity)

    def test_quantity(self):
        self.product.receive(2)
        self.product.adjust_inventory(3, 'found')
        self.product.ship(1)
        
        self.assertEqual(4, self.product.quantity)