import re
from flask import abort
from GeminiGenerator import GeminiGenerator

PROMPT = """
    {{InputText}}

    Dado o texto acima, extraia informações como Tipo de Documento, Assunto, Data, Localização, Empresa, Registro, Documentos, Nomes, Identificadores pessoais.
    Sempre que os dados forem de uma mesma entidade agrupe-os em uma mesma estrutura.
    Você deve retornar um json contendo essas informações.
"""

llm = GeminiGenerator()

def injectTextOnPrompt(inputText):
    print("Injecting text on prompt")
    inputText = str(inputText)
    templateString : str = r'{{(.*?)}}'
    replacedText : str = re.sub(pattern=templateString, 
                        repl=inputText, 
                        string=PROMPT)
    return replacedText
    
def treatResponse(response):
    # response = response.replace("\r", "").replace("\n", " ").strip()
    response = str(response)
    regex = r'{[\s\S]*}'
    match = re.search(regex, response)
    if match:
        json = match.group(0)
    else:
        json = ""
    return json

def getInfosFromText(text):

    try:
        prompt = injectTextOnPrompt(text)
        response = llm.generate(prompt)
        response = treatResponse(response)
        return response

    except Exception as e:
        print(f"Error processing request: {e}")
        abort(500, description="Error processing request")