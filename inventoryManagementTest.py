import requests
import json
import unittest
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for the CRM API
BASE_URL = "http://crmprod.baidu.com/api"
HEADERS = {"Content-Type": "application/json"}

class InventoryManagementTestCase(unittest.TestCase):

    def setUp(self):
        # Setup code to create a new product for testing
        self.product_id = self.create_product({
            "name": "Inventory Test Product",
            "description": "Product for inventory test",
            "price": 50.00,
            "stock": 200,
            "category": "Warehouse"
        })
        logging.info(f"Set up test product with ID: {self.product_id}")

    def tearDown(self):
        # Cleanup code to delete the created product
        self.delete_product(self.product_id)
        logging.info(f"Cleaned up test product with ID: {self.product_id}")

    def create_product(self, product_data):
        response = requests.post(f"{BASE_URL}/products", headers=HEADERS, data=json.dumps(product_data))
        self.assertEqual(response.status_code, 201)
        logging.info(f"Created product: {product_data}")
        return response.json()["id"]

    def delete_product(self, product_id):
        response = requests.delete(f"{BASE_URL}/products/{product_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 204)
        logging.info(f"Deleted product with ID: {product_id}")

    def add_inventory(self, inventory_data):
        response = requests.post(f"{BASE_URL}/inventory", headers=HEADERS, data=json.dumps(inventory_data))
        self.assertEqual(response.status_code, 201)
        logging.info(f"Added inventory: {inventory_data}")
        return response.json()["id"]

    def update_inventory(self, inventory_id, inventory_data):
        response = requests.put(f"{BASE_URL}/inventory/{inventory_id}", headers=HEADERS, data=json.dumps(inventory_data))
        self.assertEqual(response.status_code, 200)
        logging.info(f"Updated inventory with ID {inventory_id} to: {inventory_data}")

    def delete_inventory(self, inventory_id):
        response = requests.delete(f"{BASE_URL}/inventory/{inventory_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 204)
        logging.info(f"Deleted inventory with ID: {inventory_id}")

    def test_add_inventory(self):
        inventory_data = {
            "product_id": self.product_id,
            "quantity": 50,
            "location": "Warehouse A"
        }
        inventory_id = self.add_inventory(inventory_data)

        # Verify addition
        response = requests.get(f"{BASE_URL}/inventory/{inventory_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        inventory_info = response.json()
        self.assertEqual(inventory_info["product_id"], self.product_id)
        self.assertEqual(inventory_info["quantity"], 50)
        self.assertEqual(inventory_info["location"], "Warehouse A")
        logging.info(f"Verified inventory data: {inventory_info}")

        # Cleanup
        self.delete_inventory(inventory_id)

    def test_update_inventory(self):
        inventory_data = {
            "product_id": self.product_id,
            "quantity": 50,
            "location": "Warehouse A"
        }
        inventory_id = self.add_inventory(inventory_data)

        # Update inventory
        updated_data = {
            "quantity": 80,
            "location": "Warehouse B"
        }
        self.update_inventory(inventory_id, updated_data)

        # Verify update
        response = requests.get(f"{BASE_URL}/inventory/{inventory_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        inventory_info = response.json()
        self.assertEqual(inventory_info["quantity"], 80)
        self.assertEqual(inventory_info["location"], "Warehouse B")
        logging.info(f"Verified updated inventory data: {inventory_info}")

        # Cleanup
        self.delete_inventory(inventory_id)

    def test_list_inventory(self):
        inventory_data = {
            "product_id": self.product_id,
            "quantity": 50,
            "location": "Warehouse A"
        }
        inventory_id = self.add_inventory(inventory_data)

        # List inventory
        response = requests.get(f"{BASE_URL}/inventory", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        inventories = response.json()
        self.assertGreater(len(inventories), 0)
        logging.info(f"Listed inventories: {inventories}")

        # Cleanup
        self.delete_inventory(inventory_id)

    def test_delete_inventory(self):
        inventory_data = {
            "product_id": self.product_id,
            "quantity": 50,
            "location": "Warehouse A"
        }
        inventory_id = self.add_inventory(inventory_data)
        logging.info(f"Added inventory for deletion test with ID: {inventory_id}")

        # Delete inventory
        self.delete_inventory(inventory_id)

        # Verify deletion
        response = requests.get(f"{BASE_URL}/inventory/{inventory_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 404)
        logging.info(f"Verified inventory with ID {inventory_id} no longer exists")

if __name__ == "__main__":
    unittest.main()