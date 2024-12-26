import unittest
from flask import Flask, jsonify
from server import app
from unittest.mock import patch
from io import BytesIO

class TestServer(unittest.TestCase):

    @patch('extractInfo.getInfosFromText')
    def test_submit_data_json(self, mock_getInfosFromText):
        
        # Use app context to ensure jsonify works correctly
        with app.app_context():
            client = app.test_client()
            json_data = {"text": "Sample text"}
            
            # Act
            response = client.post('/api/submit', json=json_data)
            
            # Assert
            self.assertEqual(response.status_code, 200)

    @patch('utils.process_file')
    @patch('extractInfo.llm.generate')
    def test_submit_data_file(self, mock_process_file,mock_generateText):
        
        # Use app context to ensure jsonify works correctly
        with app.app_context():
            client = app.test_client()
            data = {
                'file': (BytesIO(b"sample file content"), 'sample.txt')
            }
            
            # Act
            response = client.post('/api/submit', data=data, content_type='multipart/form-data')
            
            # Assert
            self.assertEqual(response.status_code, 200)

    def test_submit_data_invalid(self):
        # Arrange
        client = app.test_client()
        
        # Act (sending neither JSON nor file)
        response = client.post('/api/submit', data={})
        
        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid request format"})

    @patch('extractInfo.llm.generate')
    def test_submit_data_json_exception(self, mock_generateText):
        mock_generateText.side_effect = Exception("Error")
        
        client = app.test_client()
        json_data = {"text": "Sample text"}
        
        # Act
        response = client.post('/api/submit', json=json_data)
        
        # Assert: The response should be a 500 internal server error
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
