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
You are a technical writer assistant. Use the context to draft a Medium-style article section that explains the topic clearly, thoroughly, and with a human tone.

The tone should be articulate, confident, slightly personal, and grounded in real technical insight. Avoid fluff — be practical, sharp, and helpful.

Use active voice. Prefer clarity over cleverness. It's okay to be a bit opinionated if it helps the reader.

Use emojis sparingly to enhance the tone, but don't overdo it. Use them where they add warmth or emphasis, not as a crutch.

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
