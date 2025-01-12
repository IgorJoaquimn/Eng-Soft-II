import pytest
import requests
import os
import json
from pathlib import Path

# Constants
API_URL = "http://localhost:5000"
REAL_PDF_PATH = "./test_files/real_contract.pdf"
REAL_TXT_PATH = "./test_files/real_document.txt"

class TestE2E:
    @classmethod
    def setup_class(cls):
        try:
            response = requests.get(f"{API_URL}/health")
            assert response.status_code == 200
        except requests.ConnectionError:
            pytest.fail("API server is not running")

    def test_real_pdf_upload(self):
        """
        Tests uploading a real PDF file and processing it through the entire stack
        including actual Gemini API processing
        """
        # Using a real PDF file
        with open(REAL_PDF_PATH, 'rb') as pdf:
            files = {'file': pdf}
            response = requests.post(f"{API_URL}/api/submit", files=files)
            
        assert response.status_code == 200
        data = json.loads(response.json())

        assert 'Tipo de Documento' in data
        assert 'Assunto' in data
        assert data['Tipo de Documento'] == 'Contrato'

    def test_real_text_processing(self):
        """
        Tests processing real text through the entire stack
        """
        with open(REAL_TXT_PATH, 'rb') as pdf:
            files = {'file': pdf}
            response = requests.post(f"{API_URL}/api/submit", files=files)
        
        assert response.status_code == 200
        data = json.loads(response.json())

        assert 'Tipo de Documento' in data
        assert 'Assunto' in data
        assert data['Tipo de Documento'] == 'Contrato de Prestação de Serviços'

    def test_concurrent_requests(self):
        """
        Tests how the system handles multiple simultaneous requests
        """
        import concurrent.futures
        
        def make_request():
            test_data = {"text": "Sample contract text"}
            return requests.post(f"{API_URL}/api/submit", json=test_data)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            responses = [f.result() for f in futures]
        
        # Verify all requests were successful
        assert all(r.status_code == 200 for r in responses)

    def test_error_recovery(self):
        """
        Tests system recovery after errors
        """
        # Test with malformed PDF
        with open("test_files/corrupted.pdf", 'rb') as pdf:
            files = {'file': pdf}
            response = requests.post(f"{API_URL}/api/submit", files=files)
            
        assert response.status_code in [400, 500]  # Expect error
        
        # Test system still works after error
        test_data = {"text": "Simple contract text"}
        response = requests.post(f"{API_URL}/api/submit", json=test_data)
        assert response.status_code == 200  # System recovered