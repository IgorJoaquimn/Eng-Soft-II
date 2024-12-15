import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
import os

from utils import process_file

class TestProcessFile(unittest.TestCase):

    @patch("os.makedirs")
    @patch("os.path.join")
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_process_file_success(self, mock_open, mock_path_join, mock_makedirs):
        # Setup mocks
        mock_request = MagicMock()
        mock_file = MagicMock()
        mock_file.filename = "test_file.txt"
        file_content = "This is the content of the file."
        mock_request.files.get.return_value = mock_file

        # Mock file save path
        mock_path_join.return_value = "/mock/uploads/test_file.txt"

        # Mock file saving and content
        mock_file.save = MagicMock()
        mock_open.return_value.read.return_value = file_content

        # Create a Flask app context
        app = Flask(__name__)
        with app.app_context():
            response = process_file(mock_request)

        # Assertions
        mock_file.save.assert_called_once_with("/mock/uploads/test_file.txt")
        mock_open.assert_called_once_with("/mock/uploads/test_file.txt", 'r', encoding='utf-8')

        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data[0]["filename"], "test_file.txt")
        self.assertEqual(json_data[0]["file_size"], len(file_content))

    def test_process_file_no_file(self):
        # Setup mocks
        mock_request = MagicMock()
        mock_request.files.get.return_value = None

        # Create a Flask app context
        app = Flask(__name__)
        with app.app_context():
            response = process_file(mock_request)

        # Assertions
        json_data = response[0]
        self.assertEqual(response[1], 400)
        self.assertEqual(json_data.get_json(), {"error": "No file received"})

if __name__ == "__main__":
    unittest.main()
