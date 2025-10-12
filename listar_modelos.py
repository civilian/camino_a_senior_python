import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Carga GOOGLE_API_KEY desde .env

api_key = os.environ.get("GOOGLE_API_KEY")
print("GOOGLE_API_KEY:", api_key)

genai.configure(api_key=api_key)  # <-- ¡Necesario!

models = genai.list_models()
for model in models:
    print(model.name, "-", model.supported_generation_methods)