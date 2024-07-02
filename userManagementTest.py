import requests
import json
import unittest
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for the CRM API
BASE_URL = "http://crmprod.baidu.com/api"
HEADERS = {"Content-Type": "application/json"}

class UserManagementTestCase(unittest.TestCase):

    def setUp(self):
        # Setup code to create a new user for testing
        self.user_id = self.create_user({
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "role": "user"
        })
        logging.info(f"Set up test user with ID: {self.user_id}")

    def tearDown(self):
        # Cleanup code to delete the created user
        self.delete_user(self.user_id)
        logging.info(f"Cleaned up test user with ID: {self.user_id}")

    def create_user(self, user_data):
        response = requests.post(f"{BASE_URL}/users", headers=HEADERS, data=json.dumps(user_data))
        self.assertEqual(response.status_code, 201)
        logging.info(f"Created user: {user_data}")
        return response.json()["id"]

    def delete_user(self, user_id):
        response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 204)
        logging.info(f"Deleted user with ID: {user_id}")

    def test_get_user(self):
        response = requests.get(f"{BASE_URL}/users/{self.user_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        user_data = response.json()
        self.assertEqual(user_data["username"], "testuser")
        self.assertEqual(user_data["email"], "testuser@example.com")
        self.assertEqual(user_data["role"], "user")
        logging.info(f"Retrieved user data: {user_data}")

    def test_update_user(self):
        updated_data = {
            "username": "updateduser",
            "email": "updateduser@example.com",
            "role": "admin"
        }
        response = requests.put(f"{BASE_URL}/users/{self.user_id}", headers=HEADERS, data=json.dumps(updated_data))
        self.assertEqual(response.status_code, 200)
        logging.info(f"Updated user with ID {self.user_id} to: {updated_data}")

        response = requests.get(f"{BASE_URL}/users/{self.user_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        user_data = response.json()
        self.assertEqual(user_data["username"], "updateduser")
        self.assertEqual(user_data["email"], "updateduser@example.com")
        self.assertEqual(user_data["role"], "admin")
        logging.info(f"Verified updated user data: {user_data}")

    def test_list_users(self):
        response = requests.get(f"{BASE_URL}/users", headers=HEADERS)
        self.assertEqual(response.status_code, 200)
        users = response.json()
        self.assertGreater(len(users), 0)
        logging.info(f"Listed users: {users}")

    def test_delete_user(self):
        # Create a new user for deletion test
        user_id = self.create_user({
            "username": "deletetestuser",
            "email": "deletetestuser@example.com",
            "password": "password123",
            "role": "user"
        })
        logging.info(f"Created user for deletion test with ID: {user_id}")

        # Delete the newly created user
        response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 204)
        logging.info(f"Deleted user with ID: {user_id}")

        # Verify the user no longer exists
        response = requests.get(f"{BASE_URL}/users/{user_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 404)
        logging.info(f"Verified user with ID {user_id} no longer exists")

if __name__ == "__main__":
    unittest.main()