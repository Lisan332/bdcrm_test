import requests
import json
import unittest
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for the CRM API
BASE_URL = "http://crmprod.baidu.com/api"
HEADERS = {"Content-Type": "application/json"}

class SalesOpportunityTestCase(unittest.TestCase):

    def setUp(self):
        # Setup code to create a new customer for testing
        self.customer_id = self.create_customer({
            "name": "Test Customer for Sales Opportunity",
            "email": "salesopportunity@example.com",
            "phone": "1234567890"
        })
        logging.info(f"Set up test customer with ID: {self.customer_id}")

    def tearDown(self):
        # Cleanup code to delete the created customer
        self.delete_customer(self.customer_id)
        logging.info(f"Cleaned up test customer with ID: {self.customer_id}")

    def create_customer(self, customer_data):
        response = requests.post(f"{BASE_URL}/customers", headers=HEADERS, data=json.dumps(customer_data))
        self.assertEqual(response.status_code, 201)
        logging.info(f"Created customer: {customer_data}")
        return response.json()["id"]

    def delete_customer(self, customer_id):
        response = requests.delete(f"{BASE_URL}/customers/{customer_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 204)
        logging.info(f"Deleted customer with ID: {customer_id}")

    def create_sales_opportunity(self, opportunity_data):
        response = requests.post(f"{BASE_URL}/opportunities", headers=HEADERS, data=json.dumps(opportunity_data))
        self.assertEqual(response.status_code, 201)
        logging.info(f"Created sales opportunity: {opportunity_data}")
        return response.json()["id"]

    def delete_sales_opportunity(self, opportunity_id):
        response = requests.delete(f"{BASE_URL}/opportunities/{opportunity_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 204)
        logging.info(f"Deleted sales opportunity with ID: {opportunity_id}")

    def test_create_sales_opportunity(self):
        opportunity_data = {
            "customer_id": self.customer_id,
            "title": "New Sales Opportunity",
            "description": "Potential deal with high value",
            "value": 50000,
            "status": "Open"
        }
        opportunity_id = self.create_sales_opportunity(opportunity_data)

        # Verify creation
        response = requests.get(f"{BASE_URL}/opportunities/{opportunity_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        opportunity_info = response.json()
        self.assertEqual(opportunity_info["title"], "New Sales Opportunity")
        self.assertEqual(opportunity_info["description"], "Potential deal with high value")
        self.assertEqual(opportunity_info["value"], 50000)
        self.assertEqual(opportunity_info["status"], "Open")
        logging.info(f"Verified sales opportunity data: {opportunity_info}")

        # Cleanup
        self.delete_sales_opportunity(opportunity_id)

    def test_update_sales_opportunity(self):
        opportunity_data = {
            "customer_id": self.customer_id,
            "title": "Sales Opportunity to Update",
            "description": "Initial description",
            "value": 30000,
            "status": "Open"
        }
        opportunity_id = self.create_sales_opportunity(opportunity_data)

        # Update opportunity
        updated_data = {
            "title": "Updated Sales Opportunity",
            "description": "Updated description",
            "value": 45000,
            "status": "In Progress"
        }
        response = requests.put(f"{BASE_URL}/opportunities/{opportunity_id}", headers=HEADERS, data=json.dumps(updated_data))
        self.assertEqual(response.status_code, 200)
        logging.info(f"Updated sales opportunity with ID {opportunity_id} to: {updated_data}")

        # Verify update
        response = requests.get(f"{BASE_URL}/opportunities/{opportunity_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        opportunity_info = response.json()
        self.assertEqual(opportunity_info["title"], "Updated Sales Opportunity")
        self.assertEqual(opportunity_info["description"], "Updated description")
        self.assertEqual(opportunity_info["value"], 45000)
        self.assertEqual(opportunity_info["status"], "In Progress")
        logging.info(f"Verified updated sales opportunity data: {opportunity_info}")

        # Cleanup
        self.delete_sales_opportunity(opportunity_id)

    def test_list_sales_opportunities(self):
        opportunity_data_1 = {
            "customer_id": self.customer_id,
            "title": "First Sales Opportunity",
            "description": "First deal",
            "value": 20000,
            "status": "Open"
        }
        opportunity_data_2 = {
            "customer_id": self.customer_id,
            "title": "Second Sales Opportunity",
            "description": "Second deal",
            "value": 40000,
            "status": "Open"
        }
        opportunity_id_1 = self.create_sales_opportunity(opportunity_data_1)
        opportunity_id_2 = self.create_sales_opportunity(opportunity_data_2)

        # List opportunities
        response = requests.get(f"{BASE_URL}/opportunities", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        opportunities = response.json()
        self.assertGreater(len(opportunities), 0)
        logging.info(f"Listed sales opportunities: {opportunities}")

        # Cleanup
        self.delete_sales_opportunity(opportunity_id_1)
        self.delete_sales_opportunity(opportunity_id_2)

    def test_delete_sales_opportunity(self):
        opportunity_data = {
            "customer_id": self.customer_id,
            "title": "Sales Opportunity to Delete",
            "description": "This will be deleted",
            "value": 10000,
            "status": "Open"
        }
        opportunity_id = self.create_sales_opportunity(opportunity_data)
        logging.info(f"Created sales opportunity for deletion test with ID: {opportunity_id}")

        # Delete opportunity
        self.delete_sales_opportunity(opportunity_id)

        # Verify deletion
        response = requests.get(f"{BASE_URL}/opportunities/{opportunity_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 404)
        logging.info(f"Verified sales opportunity with ID {opportunity_id} no longer exists")

if __name__ == "__main__":
    unittest.main()