import requests
import json
import unittest
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for the CRM API
BASE_URL = "http://crmprod.baidu.com/api"
HEADERS = {"Content-Type": "application/json"}

class OrderManagementTestCase(unittest.TestCase):

    def setUp(self):
        # Setup code to create a new customer and product for testing
        self.customer_id = self.create_customer({
            "name": "Order Test Customer",
            "email": "ordertest@example.com",
            "phone": "1234567890"
        })
        self.product_id = self.create_product({
            "name": "Order Test Product",
            "description": "Product for order test",
            "price": 99.99,
            "stock": 100,
            "category": "Electronics"
        })
        logging.info(f"Set up test customer with ID: {self.customer_id} and product with ID: {self.product_id}")

    def tearDown(self):
        # Cleanup code to delete the created customer and product
        self.delete_customer(self.customer_id)
        self.delete_product(self.product_id)
        logging.info(f"Cleaned up test customer with ID: {self.customer_id} and product with ID: {self.product_id}")

    def create_customer(self, customer_data):
        response = requests.post(f"{BASE_URL}/customers", headers=HEADERS, data=json.dumps(customer_data))
        self.assertEqual(response.status_code, 201)
        logging.info(f"Created customer: {customer_data}")
        return response.json()["id"]

    def delete_customer(self, customer_id):
        response = requests.delete(f"{BASE_URL}/customers/{customer_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 204)
        logging.info(f"Deleted customer with ID: {customer_id}")

    def create_product(self, product_data):
        response = requests.post(f"{BASE_URL}/products", headers=HEADERS, data=json.dumps(product_data))
        self.assertEqual(response.status_code, 201)
        logging.info(f"Created product: {product_data}")
        return response.json()["id"]

    def delete_product(self, product_id):
        response = requests.delete(f"{BASE_URL}/products/{product_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 204)
        logging.info(f"Deleted product with ID: {product_id}")

    def create_order(self, order_data):
        response = requests.post(f"{BASE_URL}/orders", headers=HEADERS, data=json.dumps(order_data))
        self.assertEqual(response.status_code, 201)
        logging.info(f"Created order: {order_data}")
        return response.json()["id"]

    def delete_order(self, order_id):
        response = requests.delete(f"{BASE_URL}/orders/{order_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 204)
        logging.info(f"Deleted order with ID: {order_id}")

    def test_create_order(self):
        order_data = {
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": 1,
            "total_price": 99.99,
            "status": "Pending"
        }
        order_id = self.create_order(order_data)

        # Verify creation
        response = requests.get(f"{BASE_URL}/orders/{order_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        order_info = response.json()
        self.assertEqual(order_info["customer_id"], self.customer_id)
        self.assertEqual(order_info["product_id"], self.product_id)
        self.assertEqual(order_info["quantity"], 1)
        self.assertEqual(order_info["total_price"], 99.99)
        self.assertEqual(order_info["status"], "Pending")
        logging.info(f"Verified order data: {order_info}")

        # Cleanup
        self.delete_order(order_id)

    def test_update_order(self):
        order_data = {
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": 1,
            "total_price": 99.99,
            "status": "Pending"
        }
        order_id = self.create_order(order_data)

        # Update order
        updated_data = {
            "quantity": 2,
            "total_price": 199.98,
            "status": "Confirmed"
        }
        response = requests.put(f"{BASE_URL}/orders/{order_id}", headers=HEADERS, data=json.dumps(updated_data))
        self.assertEqual(response.status_code, 200)
        logging.info(f"Updated order with ID {order_id} to: {updated_data}")

        # Verify update
        response = requests.get(f"{BASE_URL}/orders/{order_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        order_info = response.json()
        self.assertEqual(order_info["quantity"], 2)
        self.assertEqual(order_info["total_price"], 199.98)
        self.assertEqual(order_info["status"], "Confirmed")
        logging.info(f"Verified updated order data: {order_info}")

        # Cleanup
        self.delete_order(order_id)

    def test_list_orders(self):
        order_data = {
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": 1,
            "total_price": 99.99,
            "status": "Pending"
        }
        order_id = self.create_order(order_data)

        # List orders
        response = requests.get(f"{BASE_URL}/orders", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        orders = response.json()
        self.assertGreater(len(orders), 0)
        logging.info(f"Listed orders: {orders}")

        # Cleanup
        self.delete_order(order_id)

    def test_delete_order(self):
        order_data = {
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": 1,
            "total_price": 99.99,
            "status": "Pending"
        }
        order_id = self.create_order(order_data)
        logging.info(f"Created order for deletion test with ID: {order_id}")

        # Delete order
        self.delete_order(order_id)

        # Verify deletion
        response = requests.get(f"{BASE_URL}/orders/{order_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 404)
        logging.info(f"Verified order with ID {order_id} no longer exists")

if __name__ == "__main__":
    unittest.main()