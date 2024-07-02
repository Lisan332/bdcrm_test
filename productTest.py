import requests
import json
import unittest
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for the CRM API
BASE_URL = "http://crmprod.baidu.com/api"
HEADERS = {"Content-Type": "application/json"}


class ProductManagementTestCase(unittest.TestCase):

    def setUp(self):
        # Setup code to create a new product for testing
        self.product_id = self.create_product({
            "name": "Test Product",
            "description": "This is a test product",
            "price": 99.99,
            "stock": 100,
            "category": "Electronics"
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

    def test_get_product(self):
        response = requests.get(f"{BASE_URL}/products/{self.product_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        product_data = response.json()
        self.assertEqual(product_data["name"], "Test Product")
        self.assertEqual(product_data["description"], "This is a test product")
        self.assertEqual(product_data["price"], 99.99)
        self.assertEqual(product_data["stock"], 100)
        self.assertEqual(product_data["category"], "Electronics")
        logging.info(f"Retrieved product data: {product_data}")

    def test_update_product(self):
        updated_data = {
            "name": "Updated Test Product",
            "description": "Updated description",
            "price": 89.99,
            "stock": 150,
            "category": "Gadgets"
        }
        response = requests.put(f"{BASE_URL}/products/{self.product_id}", headers=HEADERS,
                                data=json.dumps(updated_data))
        self.assertEqual(response.status_code, 200)
        logging.info(f"Updated product with ID {self.product_id} to: {updated_data}")

        response = requests.get(f"{BASE_URL}/products/{self.product_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        product_data = response.json()
        self.assertEqual(product_data["name"], "Updated Test Product")
        self.assertEqual(product_data["description"], "Updated description")
        self.assertEqual(product_data["price"], 89.99)
        self.assertEqual(product_data["stock"], 150)
        self.assertEqual(product_data["category"], "Gadgets")
        logging.info(f"Verified updated product data: {product_data}")

    def test_list_products(self):
        response = requests.get(f"{BASE_URL}/products", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        products = response.json()
        self.assertGreater(len(products), 0)
        logging.info(f"Listed products: {products}")

    def test_delete_product(self):
        # Create a new product for deletion test
        product_id = self.create_product({
            "name": "Delete Test Product",
            "description": "This product will be deleted",
            "price": 49.99,
            "stock": 10,
            "category": "Misc"
        })
        logging.info(f"Created product for deletion test with ID: {product_id}")

        # Delete the newly created product
        response = requests.delete(f"{BASE_URL}/products/{product_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 204)
        logging.info(f"Deleted product with ID: {product_id}")

        # Verify the product no longer exists
        response = requests.get(f"{BASE_URL}/products/{product_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 404)
        logging.info(f"Verified product with ID {product_id} no longer exists")


if __name__ == "__main__":
    unittest.main()