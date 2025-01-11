import os
from flask import abort
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv('../.env')

API_KEY= os.getenv('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)

class GeminiGenerator:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
    def generate(self, prompt):
        try:
            print(f"Gemini prompt: {prompt}")
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=5000,
                    temperature=0.2,
                    top_p=0.9
                ),
            )
            print(f"Gemini response: {response.text}")
            return response.text
        
        except Exception as e:
            print(f"Error making request to Google Gemini: {e}")
            abort(400, description="Invalid request")
