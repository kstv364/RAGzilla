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

def summarize_text(text, video_title="", summary_type="study_guide"):
    study_guide_prompt = f"""
You are an expert academic content creator tasked with converting a one-way lecture transcript into comprehensive, exam-ready study material. The lecture is pre-recorded, so the transcript is a monologue.

Your objectives:

Detailed Pointwise Notes:

Organize into clear headings, subheadings, and bullet points.

Retain all important definitions, formulas, steps, examples, and facts without omitting details.

Remove conversational fillers and redundant phrases.

Use bold for important terms, italics for definitions.

Break down complex concepts into smaller, digestible points.

After each section, create a Quick Revision – Flash Points list with only the most crucial facts from that section.

The final output should read like a complete, structured study guide that can be used without listening to the lecture again.

{"Video Title: " + video_title if video_title else ""}
Transcript:
{text}
"""

    detailed_transcript_prompt = f"""
You are an expert summarizer tasked with creating a highly detailed and comprehensive summary of a lecture transcript. The goal is to provide a thorough overview that retains all critical information, nuances, and specific examples from the original content.

Your objectives:

1.  **Comprehensive Coverage**: Ensure all major points, sub-points, and supporting details are included. Do not omit any significant information.
2.  **Structured Format**: Organize the summary logically with clear headings, subheadings, and bullet points where appropriate.
3.  **Accuracy**: Reflect the original content accurately, maintaining the original meaning and context.
4.  **Clarity and Conciseness**: While detailed, the summary should be clear, easy to understand, and free of conversational fillers or redundant phrases.
5.  **Key Terminology**: Highlight important terms and concepts.
6.  **Examples and Explanations**: Include specific examples, analogies, and explanations provided in the transcript to illustrate concepts.
7.  **Flow**: Ensure a smooth transition between topics.

The final output should be a standalone document that provides a complete and detailed understanding of the lecture, suitable for someone who needs to grasp the full scope of the content without listening to the original lecture.

{"Video Title: " + video_title if video_title else ""}
Transcript:
{text}
"""

    prompt = study_guide_prompt if summary_type == "study_guide" else detailed_transcript_prompt
    
    use_gemini = os.getenv("USE_GEMINI", "true").lower() == "true"

    llm_output = "No summary found"

    if use_gemini and GEMINI_API_KEY:
        print(f"Using Gemini API for {summary_type} summarization")
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            llm_output = response.text
        except Exception as e:
            logger.error(f"Gemini API error during summarization: {e}. Falling back to Ollama.")
            use_gemini = False # Fallback if Gemini fails
    
    if not use_gemini:
        print(f"Falling back to Ollama for {summary_type} summarization")
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True
        )
        llm_output = result.stdout.strip()

    # Write summary to a .md file
    import uuid
    import re
    if video_title:
        # Sanitize title for filename
        filename = re.sub(r'[^\w\s-]', '', video_title).strip().replace(' ', '_')
        if not filename: # Fallback if title becomes empty after sanitization
            filename = str(uuid.uuid4())
    else:
        filename = str(uuid.uuid4())
    
    file_path = f"summaries/{filename}.md"
    os.makedirs("summaries", exist_ok=True) # Ensure 'summaries' directory exists
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(llm_output)
    logger.info(f"Summary saved to {file_path}")

    return {"summary": llm_output, "summary_file": file_path}
