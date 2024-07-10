import requests
import json
import unittest
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for the CRM API
BASE_URL = "http://crmprod.baidu.com/api"
HEADERS = {"Content-Type": "application/json"}


class CRMTestCase(unittest.TestCase):

    def setUp(self):
        # Setup code to create a new customer for testing
        self.customer_id = self.create_customer({
            "name": "Test Customer",
            "email": "testcustomer@example.com",
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

    def test_get_customer(self):
        response = requests.get(f"{BASE_URL}/customers/{self.customer_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        customer_data = response.json()
        self.assertEqual(customer_data["name"], "Test Customer")
        self.assertEqual(customer_data["email"], "testcustomer@example.com")
        self.assertEqual(customer_data["phone"], "1234567890")
        logging.info(f"Retrieved customer data: {customer_data}")

    def test_update_customer(self):
        updated_data = {
            "name": "Updated Test Customer",
            "email": "updatedcustomer@example.com",
            "phone": "0987654321"
        }
        response = requests.put(f"{BASE_URL}/customers/{self.customer_id}", headers=HEADERS,
                                data=json.dumps(updated_data))
        self.assertEqual(response.status_code, 200)
        logging.info(f"Updated customer with ID {self.customer_id} to: {updated_data}")

        response = requests.get(f"{BASE_URL}/customers/{self.customer_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        customer_data = response.json()
        self.assertEqual(customer_data["name"], "Updated Test Customer")
        self.assertEqual(customer_data["email"], "updatedcustomer@example.com")
        self.assertEqual(customer_data["phone"], "0987654321")
        logging.info(f"Verified updated customer data: {customer_data}")

    def test_list_customers(self):
        response = requests.get(f"{BASE_URL}/customers", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        customers = response.json()
        self.assertGreater(len(customers), 0)
        logging.info(f"Listed customers: {customers}")

    def test_delete_customer(self):
        # Create a new customer for deletion test
        customer_id = self.create_customer({
            "name": "Delete Test Customer",
            "email": "deletetestcustomer@example.com",
            "phone": "1234567890"
        })
        logging.info(f"Created customer for deletion test with ID: {customer_id}")

        # Delete the newly created customer
        response = requests.delete(f"{BASE_URL}/customers/{customer_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 204)
        logging.info(f"Deleted customer with ID: {customer_id}")

        # Verify the customer no longer exists
        response = requests.get(f"{BASE_URL}/customers/{customer_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 404)
        logging.info(f"Verified customer with ID {customer_id} no longer exists")

    def test_assign_task_to_customer(self):
        task_data = {
            "description": "Follow up call",
            "due_date": "2023-12-31"
        }
        response = requests.post(f"{BASE_URL}/customers/{self.customer_id}/tasks", headers=HEADERS,
                                 data=json.dumps(task_data))
        self.assertEqual(response.status_code, 201)
        task_id = response.json()["id"]
        logging.info(f"Assigned task {task_data} with ID {task_id} to customer {self.customer_id}")

        # Verify task assignment
        response = requests.get(f"{BASE_URL}/customers/{self.customer_id}/tasks/{task_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        task_info = response.json()
        self.assertEqual(task_info["description"], "Follow up call")
        self.assertEqual(task_info["due_date"], "2023-12-31")
        logging.info(f"Verified assigned task data: {task_info}")

    def test_update_customer_status(self):
        status_data = {"status": "Active"}
        response = requests.patch(f"{BASE_URL}/customers/{self.customer_id}/status", headers=HEADERS,
                                  data=json.dumps(status_data))
        self.assertEqual(response.status_code, 200)
        logging.info(f"Updated customer {self.customer_id} status to: {status_data}")

        # Verify status update
        response = requests.get(f"{BASE_URL}/customers/{self.customer_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        customer_data = response.json()
        self.assertEqual(customer_data["status"], "Active")
        logging.info(f"Verified customer status: {customer_data['status']}")

    def test_handle_customer_complaint(self):
        complaint_data = {
            "description": "Product not delivered",
            "date": "2023-11-30"
        }
        response = requests.post(f"{BASE_URL}/customers/{self.customer_id}/complaints", headers=HEADERS,
                                 data=json.dumps(complaint_data))
        self.assertEqual(response.status_code, 201)
        complaint_id = response.json()["id"]
        logging.info(f"Logged complaint {complaint_data} with ID {complaint_id} for customer {self.customer_id}")

        # Verify complaint logging
        response = requests.get(f"{BASE_URL}/customers/{self.customer_id}/complaints/{complaint_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        complaint_info = response.json()
        self.assertEqual(complaint_info["description"], "Product not delivered")
        self.assertEqual(complaint_info["date"], "2023-11-30")
        logging.info(f"Verified logged complaint data: {complaint_info}")

    def test_customer_interaction_history(self):
        # Create an interaction
        interaction_data = {
            "type": "Email",
            "content": "Sent product catalog",
            "date": "2023-10-10"
        }
        response = requests.post(f"{BASE_URL}/customers/{self.customer_id}/interactions", headers=HEADERS,
                                 data=json.dumps(interaction_data))
        self.assertEqual(response.status_code, 201)
        interaction_id = response.json()["id"]
        logging.info(f"Logged interaction {interaction_data} with ID {interaction_id} for customer {self.customer_id}")

        # List interactions
        response = requests.get(f"{BASE_URL}/customers/{self.customer_id}/interactions", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        interactions = response.json()
        self.assertGreater(len(interactions), 0)
        logging.info(f"Listed interactions for customer {self.customer_id}: {interactions}")

    def test_customer_notes(self):
        # Add a note
        note_data = {
            "content": "Customer prefers email communication",
            "date": "2023-10-15"
        }
        response = requests.post(f"{BASE_URL}/customers/{self.customer_id}/notes", headers=HEADERS,
                                 data=json.dumps(note_data))
        self.assertEqual(response.status_code, 201)
        note_id = response.json()["id"]
        logging.info(f"Added note {note_data} with ID {note_id} to customer {self.customer_id}")

        # List notes
        response = requests.get(f"{BASE_URL}/customers/{self.customer_id}/notes", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        notes = response.json()
        self.assertGreater(len(notes), 0)
        logging.info(f"Listed notes for customer {self.customer_id}: {notes}")

    def test_customer_attachments(self):
        # Upload an attachment
        attachment_data = {
            "filename": "contract.pdf",
            "filetype": "application/pdf",
            "content": "base64_encoded_content_here"
        }
        response = requests.post(f"{BASE_URL}/customers/{self.customer_id}/attachments", headers=HEADERS,
                                 data=json.dumps(attachment_data))
        self.assertEqual(response.status_code, 201)
        attachment_id = response.json()["id"]
        logging.info(f"Uploaded attachment {attachment_data} with ID {attachment_id} for customer {self.customer_id}")

        # List attachments
        response = requests.get(f"{BASE_URL}/customers/{self.customer_id}/attachments", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        attachments = response.json()
        self.assertGreater(len(attachments), 0)
        logging.info(f"Listed attachments for customer {self.customer_id}: {attachments}")

    def test_customer_custom_fields(self):
        # Add a custom field
        custom_field_data = {
            "field_name": "Preferred Language",
            "field_value": "English"
        }
        response = requests.post(f"{BASE_URL}/customers/{self.customer_id}/custom_fields", headers=HEADERS,
                                 data=json.dumps(custom_field_data))
        self.assertEqual(response.status_code, 201)
        custom_field_id = response.json()["id"]
        logging.info(f"Added custom field {custom_field_data} with ID {custom_field_id} to customer {self.customer_id}")

        # List custom fields
        response = requests.get(f"{BASE_URL}/customers/{self.customer_id}/custom_fields", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        custom_fields = response.json()
        self.assertGreater(len(custom_fields), 0)
        logging.info(f"Listed custom fields for customer {self.customer_id}: {custom_fields}")


if __name__ == "__main__":
    unittest.main()