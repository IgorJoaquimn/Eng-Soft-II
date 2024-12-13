import unittest
from unittest.mock import MagicMock
from GeminiGenerator import GeminiGenerator
from extractInfo import *


class TestGeminiFunctions(unittest.TestCase):
    def setUp(self):
        # Mock the GeminiGenerator
        self.mock_llm = MagicMock(spec=GeminiGenerator)
        self.test_text = "Teste de entrada para extração de informações."
        self.mock_response = '{"Tipo de Documento": "Nota", "Data": "2024-12-13"}'

    def test_injectTextOnPrompt(self):
        injected_prompt = injectTextOnPrompt(self.test_text)
        expected_prompt = PROMPT.replace("{{InputText}}", self.test_text)
        self.assertEqual(injected_prompt, expected_prompt)

    def test_treatResponse_valid_json(self):
        treated_response = treatResponse(self.mock_response)
        self.assertEqual(treated_response, self.mock_response)

    def test_treatResponse_no_json(self):
        invalid_response = "No JSON here!"
        treated_response = treatResponse(invalid_response)
        self.assertEqual(treated_response, "")

    def test_getInfosFromText(self):
        # Patch the GeminiGenerator's generate method
        self.mock_llm.generate.return_value = self.mock_response
        prompt = injectTextOnPrompt(self.test_text)
        response = self.mock_llm.generate(prompt)
        treated_response = treatResponse(response)
        self.assertEqual(treated_response, self.mock_response)

if __name__ == "__main__":
    unittest.main()

