import os
import re

# Si quieres usar Gemini vía LangChain, necesitas instalar:
# pip install langchain-google-genai google-generativeai python-dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv  # <-- Añadido para cargar .env

INPUT_FILE = "habilidades_python.md"
OUTPUT_DIR = "conceptos"

def to_snake_case(text):
    text = text.strip().replace("/", " ")
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", "_", text)
    return text.lower()

def is_concept_line(line):
    line = line.strip()
    return line.startswith("-") and len(line) > 2

def extract_concept(line):
    return line.lstrip("-").strip()

def get_gemini_response(concept, llm):
    prompt = (
        f"Enséñame sobre {concept} lo más profundo posible, "
        "lo suficiente para volverme senior en programación."
        "Devuelvelo en formato MD."
        "Incluye la mayor cantidad de citaciones reales posibles."
    )
    response = llm.invoke(prompt)
    return response.content if hasattr(response, "content") else str(response)

def main():
    load_dotenv()  # <-- Carga variables de entorno desde .env
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Configura tu API KEY de Gemini en la variable de entorno GOOGLE_API_KEY
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-pro", temperature=0.5)
    with open(INPUT_FILE, encoding="utf-8") as f:
        for line in f:
            if is_concept_line(line):
                concept = extract_concept(line)
                filename = to_snake_case(concept) + ".md"
                filepath = os.path.join(OUTPUT_DIR, filename)
                print(f"Generando: {filepath}")
                respuesta = get_gemini_response(concept, llm)
                with open(filepath, "w", encoding="utf-8") as out:
                    out.write(f"# {concept}\n\n{respuesta}\n")

if __name__ == "__main__":
    main()