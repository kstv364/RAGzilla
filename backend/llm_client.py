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

def summarize_text(text, video_title="", summary_type="study_guide", language="en"):
    study_guide_prompt = f"""
You are an expert academic content creator tasked with converting a one-way lecture transcript into comprehensive, exam-ready study material. The lecture is pre-recorded, so the transcript is a monologue. The output should be in {language}.

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
You are an expert summarizer tasked with creating a highly detailed and comprehensive summary of a lecture transcript. The goal is to provide a thorough overview that retains all critical information, nuances, and specific examples from the original content. The output should be in {language}.

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

    cloud_expertise_article_prompt = f"""
You are an expert software engineer tasked with writing a comprehensive Medium article based on the provided lecture transcript. The article should showcase your expertise in **Cloud Technologies**.

Your objectives:

1.  **Target Audience**: Software engineers, cloud architects, and tech enthusiasts.
2.  **Structure**:
    *   Catchy Title (H1 equivalent, use `# `)
    *   Introduction (hook, what the article covers)
    *   Main Body (organized with clear headings and subheadings. Use `## ` for main sections and `### ` for sub-sections. Do not use more than two heading levels apart from the title.)
    *   Conclusion (key takeaways, future outlook)
3.  **Content Focus**:
    *   Extract key concepts related to cloud computing (e.g., AWS, Azure, GCP, serverless, microservices, containerization, infrastructure as code, cloud security, cost optimization, distributed systems).
    *   Explain these concepts clearly and concisely.
    *   **Include real-life code examples** where applicable (e.g., a snippet of a serverless function, a basic IaC template, a design pattern implementation relevant to cloud). Ensure code examples are placed naturally within the reading flow, typically after an explanation of the concept they illustrate. Use Python, Node.js, or Go for code examples.
    *   **Include architecture diagrams** (described in text, e.g., "A typical serverless architecture would involve API Gateway -> Lambda -> DynamoDB").
    *   Discuss best practices, common pitfalls, and solutions in cloud development.
    *   Showcase your understanding of cloud design patterns (e.g., Strangler Fig, Circuit Breaker, Saga).
    *   **Use single-level bullet points only.** Do not use nested bullet points.
4.  **Tone**: Professional, insightful, and engaging.
5.  **Length**: Aim for a comprehensive article suitable for Medium (e.g., 1500-2500 words, adjust based on content).

{"Video Title: " + video_title if video_title else ""}
Transcript:
{text}
"""

    ai_ml_expertise_article_prompt = f"""
You are an expert software engineer tasked with writing a comprehensive Medium article based on the provided lecture transcript. The article should showcase your expertise in **AI/ML Technologies**.

Your objectives:

1.  **Target Audience**: Software engineers, data scientists, ML engineers, and AI enthusiasts.
2.  **Structure**:
    *   Catchy Title (H1 equivalent, use `# `)
    *   Introduction (hook, what the article covers)
    *   Main Body (organized with clear headings and subheadings. Use `## ` for main sections and `### ` for sub-sections. Do not use more than two heading levels apart from the title.)
    *   Conclusion (key takeaways, future outlook)
3.  **Content Focus**:
    *   Extract key concepts related to AI/ML (e.g., machine learning algorithms, deep learning, neural networks, NLP, computer vision, model deployment, MLOps, data preprocessing, ethical AI).
    *   Explain these concepts clearly and concisely.
    *   **Include real-life code examples** where applicable (e.g., a simple Python snippet for a model training loop, a data preprocessing step, a design pattern for ML pipelines). Ensure code examples are placed naturally within the reading flow, typically after an explanation of the concept they illustrate. Use Python for code examples.
    *   **Include architecture diagrams** (described in text, e.g., "A typical ML pipeline involves Data Ingestion -> Data Preprocessing -> Model Training -> Model Evaluation -> Model Deployment").
    *   Discuss best practices, common challenges, and solutions in AI/ML development.
    *   Showcase your understanding of ML design patterns (e.g., Feature Store, Model Versioning, Online/Offline Inference).
    *   **Use single-level bullet points only.** Do not use nested bullet points.
4.  **Tone**: Professional, insightful, and engaging.
5.  **Length**: Aim for a comprehensive article suitable for Medium (e.g., 1500-2500 words, adjust based on content).

{"Video Title: " + video_title if video_title else ""}
Transcript:
{text}
"""

    if summary_type == "study_guide":
        prompt = study_guide_prompt
    elif summary_type == "detailed_transcript":
        prompt = detailed_transcript_prompt
    elif summary_type == "medium_article_cloud":
        prompt = cloud_expertise_article_prompt
    elif summary_type == "medium_article_ai_ml":
        prompt = ai_ml_expertise_article_prompt
    else:
        prompt = study_guide_prompt # Default fallback
    
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

    # Determine the subfolder based on summary_type
    subfolder = ""
    if summary_type == "study_guide":
        subfolder = "study_guides"
    elif summary_type == "detailed_transcript":
        subfolder = "detailed_transcripts"
    elif summary_type == "medium_article_cloud":
        subfolder = "medium_articles_cloud"
    elif summary_type == "medium_article_ai_ml":
        subfolder = "medium_articles_ai_ml"
    else:
        subfolder = "misc_summaries" # Fallback for any unhandled types

    base_dir = "summaries"
    output_dir = os.path.join(base_dir, subfolder)
    os.makedirs(output_dir, exist_ok=True) # Ensure the specific subfolder exists

    if video_title:
        # Sanitize title for filename
        filename = re.sub(r'[^\w\s-]', '', video_title).strip().replace(' ', '_')
        if not filename: # Fallback if title becomes empty after sanitization
            filename = str(uuid.uuid4())
    else:
        filename = str(uuid.uuid4())
    
    file_path = os.path.join(output_dir, f"{filename}{str(uuid.uuid4())}.md")
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(llm_output)
    logger.info(f"Summary saved to {file_path}")

    return {"summary": llm_output, "summary_file": file_path}

def generate_ai_ml_posts(content: str, user_prompt: str):
    post_generation_prompt = f"""
You are an expert AI/ML thought leader. Your task is to generate 3 distinct short posts (50-100 words each) based on the provided content and user prompt. Each post should:
- Focus on AI/ML concepts.
- Be insightful and demonstrate technical leadership.
- Be concise and suitable for platforms like LinkedIn.
- Incorporate the user's specific prompt or focus.
- Address the broad concept from 3 different angles or perspectives.
- Use professional emojis sparingly to enhance readability and engagement.
- Be structured with appropriate spacing (e.g., short paragraphs, line breaks) for a clean, catchy presentation on LinkedIn.

Content:
{content}

User Prompt:
{user_prompt}

Generate 3 posts, each clearly separated by "---POST---".

Example format:
Post 1 content.
---POST---
Post 2 content.
---POST---
Post 3 content.
"""
    
    use_gemini = os.getenv("USE_GEMINI", "true").lower() == "true"
    posts_output = ""

    if use_gemini and GEMINI_API_KEY:
        logger.info("Using Gemini API for AI/ML post generation.")
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(post_generation_prompt)
            posts_output = response.text
        except Exception as e:
            logger.error(f"Gemini API error during AI/ML post generation: {e}. Falling back to Ollama.")
            use_gemini = False
    
    if not use_gemini:
        logger.info("Falling back to Ollama for AI/ML post generation.")
        result = subprocess.run(
            ["ollama", "run", "llama3", post_generation_prompt],
            capture_output=True,
            text=True
        )
        posts_output = result.stdout.strip()

    # Parse the output into a list of posts
    posts = [p.strip() for p in posts_output.split("---POST---") if p.strip()]
    return posts
