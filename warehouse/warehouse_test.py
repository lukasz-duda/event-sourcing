import unittest

from warehouse.warehouse_product import WarehouseProduct

class WarehouseTest(unittest.TestCase):

    def test_warehouse_product(self):
        product = WarehouseProduct('a')
        self.assertEqual('a', product.sku)