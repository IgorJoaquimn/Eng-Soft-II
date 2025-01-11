import unittest
from unittest.mock import MagicMock, patch
from flask import Flask
from werkzeug.exceptions import BadRequest


from utils import process_file, validate_file_input

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
        mock_open.assert_called_once_with("/mock/uploads/test_file.txt", 'r', encoding='UTF-8', errors='ignore')

    def test_no_file_received(self):
        # Test for no file in the request
        mock_request = MagicMock()
        mock_request.files.get.return_value = None

        # Create a Flask app context
        app = Flask(__name__)
        with app.app_context():
            with self.assertRaises(BadRequest) as context:
                validate_file_input(mock_request)

            self.assertEqual(context.exception.description, "No file received")

    def test_empty_filename(self):
        # Simulate the request with an empty filename
        mock_request = MagicMock()
        mock_request.files.get.return_value = MagicMock(filename="")

        # Create a Flask app context
        app = Flask(__name__)
        with app.app_context():
            with self.assertRaises(BadRequest) as context:
                validate_file_input(mock_request)

            self.assertEqual(context.exception.description, "Empty filename")

    def test_unsupported_file_type(self):
        mock_request = MagicMock()
        mock_file = MagicMock()
        mock_file.filename = "example.exe"
        mock_request.files.get.return_value = mock_file

        # Create a Flask app context
        app = Flask(__name__)
        with app.app_context():
            with self.assertRaises(BadRequest) as context:
                validate_file_input(mock_request)

            self.assertEqual(context.exception.description, "Unsupported file type")
    
    

if __name__ == "__main__":
    unittest.main()
