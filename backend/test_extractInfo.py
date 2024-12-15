from extractInfo import *
from unittest.mock import MagicMock
import unittest


class TestGeminiExtractor(unittest.TestCase):
    def test_injectTextOnPrompt(self):
        inputText = "Documento: Contrato de Aluguel\nData: 15/12/2024"
        expected_prompt = ("""
    Documento: Contrato de Aluguel
Data: 15/12/2024

    Dado o texto acima, extraia informações como Tipo de Documento, Assunto, Data, Localização, Empresa, Registro, Documentos, Nomes, Identificadores pessoais.
    Sempre que os dados forem de uma mesma entidade agrupe-os em uma mesma estrutura.
    Você deve retornar um json contendo essas informações.
""")
        result = injectTextOnPrompt(inputText)
        self.assertEqual(result, expected_prompt)

    def test_treatResponse_with_json(self):
        response = """
        Aqui está sua resposta:
        {
            "Tipo de Documento": "Contrato",
            "Data": "15/12/2024"
        }
        """
        expected_json = '{"Tipo de Documento": "Contrato", "Data": "15/12/2024"}'
        result = treatResponse(response)
        self.assertEqual(result, expected_json)

    def test_treatResponse_without_json(self):
        response = "Nenhum dado encontrado."
        expected_json = ""
        result = treatResponse(response)
        self.assertEqual(result, expected_json)

    def test_getInfosFromText(self):
        # Mocking GeminiGenerator.generate
        inputText = "Documento: Contrato de Aluguel\nData: 15/12/2024"
        llm.generate = MagicMock(return_value="""
        {
            "Tipo de Documento": "Contrato",
            "Data": "15/12/2024"
        }
        """)

        expected_json = '{"Tipo de Documento": "Contrato", "Data": "15/12/2024"}'
        result = getInfosFromText(inputText)
        self.assertEqual(result, expected_json)


if __name__ == '__main__':
    _ = unittest.main()
