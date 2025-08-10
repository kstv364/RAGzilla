import subprocess
import os
import google.generativeai as genai
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
load_dotenv()
# Configure Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API configured.")
else:
    logger.warning("GEMINI_API_KEY not found. Gemini will not be used unless configured.")

def generate_answer(query, context):
    prompt = f"""
You are an expert research assistant. You are given the following information, and you must answer the question based on it.

Context:
{context}

Write a clear and solid explanation or answer to this prompt:
{query}
"""
    
    use_gemini = os.getenv("USE_GEMINI", "true").lower() == "true"

    llm_output = "No answer found"

    if use_gemini and GEMINI_API_KEY:
        print("Using Gemini API")
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            llm_output = response.text
        except Exception as e:
            logger.error(f"Gemini API error: {e}. Falling back to Ollama.")
            use_gemini = False # Fallback if Gemini fails
    
    if not use_gemini:
        print("Falling back to Ollama")
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True
        )
        llm_output = result.stdout.strip()

    with open("output.md", "w", encoding='utf-8') as f:
      f.write(llm_output)
    return {"answer": llm_output}

def summarize_text(text):
    prompt = f"""
Please provide a concise summary of the following text.

Text:
{text}
"""
    
    use_gemini = os.getenv("USE_GEMINI", "true").lower() == "true"

    llm_output = "No summary found"

    if use_gemini and GEMINI_API_KEY:
        print("Using Gemini API for summarization")
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            llm_output = response.text
        except Exception as e:
            logger.error(f"Gemini API error during summarization: {e}. Falling back to Ollama.")
            use_gemini = False # Fallback if Gemini fails
    
    if not use_gemini:
        print("Falling back to Ollama for summarization")
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True
        )
        llm_output = result.stdout.strip()

    return {"summary": llm_output}
