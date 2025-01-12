import unittest
import requests
import os
import json
from pathlib import Path
import concurrent.futures

# Constants
API_URL = "http://localhost:5000"
REAL_PDF_PATH = "tests/test_files/real_contract.pdf"
CORRUPTED_PDF_PATH = "tests/test_files/corrupted.pdf"
REAL_TXT_PATH = "tests/test_files/real_document.txt"

class TestE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        try:
            response = requests.get(f"{API_URL}/health")
            if response.status_code != 200:
                raise unittest.SkipTest("API server is not healthy")
        except requests.ConnectionError:
            raise unittest.SkipTest("API server is not running")

    def setUp(self):
        """Run before each test"""
        # Verify required test files exist
        self.assertTrue(os.path.exists(REAL_PDF_PATH), "Real PDF test file not found")
        self.assertTrue(os.path.exists(REAL_TXT_PATH), "Real TXT test file not found")
        self.assertTrue(os.path.exists(CORRUPTED_PDF_PATH), "Corrupted PDF test file not found")

    def test_real_pdf_upload(self):
        """Tests uploading a real PDF file and processing it through the entire stack"""
        with open(REAL_PDF_PATH, 'rb') as pdf:
            files = {'file': pdf}
            response = requests.post(f"{API_URL}/api/submit", files=files)
            
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.json())

        self.assertIn('Tipo de Documento', data)
        self.assertIn('Assunto', data)
        self.assertEqual(data['Tipo de Documento'], 'Contrato')

    def test_real_text_processing(self):
        """Tests processing real text through the entire stack"""
        with open(REAL_TXT_PATH, 'rb') as txt:
            files = {'file': txt}
            response = requests.post(f"{API_URL}/api/submit", files=files)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.json())

        self.assertIn('Tipo de Documento', data)
        self.assertIn('Assunto', data)
        self.assertEqual(data['Tipo de Documento'], 'Contrato de Prestação de Serviços')

    def test_concurrent_requests(self):
        """Tests how the system handles multiple simultaneous requests"""
        def make_request():
            test_data = {"text": "Sample contract text"}
            return requests.post(f"{API_URL}/api/submit", json=test_data)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            responses = [f.result() for f in futures]
        
        # Verify all requests were successful
        for response in responses:
            self.assertEqual(response.status_code, 200)

    def test_error_recovery(self):
        """Tests system recovery after errors"""
        # Test with malformed PDF
        with open(CORRUPTED_PDF_PATH, 'rb') as pdf:
            files = {'file': pdf}
            response = requests.post(f"{API_URL}/api/submit", files=files)
            
        self.assertIn(response.status_code, [400, 500])  # Expect error
        
        # Test system still works after error
        test_data = {"text": "Simple contract text"}
        response = requests.post(f"{API_URL}/api/submit", json=test_data)
        self.assertEqual(response.status_code, 200)  # System recovered

if __name__ == '__main__':
    unittest.main(verbosity=2)