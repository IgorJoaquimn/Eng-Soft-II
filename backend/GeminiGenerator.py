import os
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
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=5000,
                    temperature=0.2,
                    top_p=0.9
                ),
            )
            return response.text
            
        except:
            print(f"Error making request to Google Gemini")
            return None