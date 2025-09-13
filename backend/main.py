from fastapi import FastAPI, UploadFile, File, Form
from backend.ingest import ingest_pdf, ingest_youtube
from backend.rag import answer_query
from backend.llm_client import summarize_text
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from dotenv import load_dotenv
import os
import logging
from backend.humanizer import humanize_article_with_langgraph # Import the new function
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info("Environment variables loaded from .env file.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ingest-pdf")
async def ingest_pdf_route(file: UploadFile = File(...), collection_name: Optional[str] = Form("docs")):
    content = await file.read()
    return ingest_pdf(file.filename, content, collection_name)

@app.post("/ingest-youtube")
async def ingest_youtube_route(
    youtube_url: str = Form(...),
    collection_name: Optional[str] = Form("docs"),
    summary_type: Optional[str] = Form("study_guide"), # New parameter for summary type
    language: Optional[str] = Form("en") # New parameter for language
):
    ingestion_result = ingest_youtube(youtube_url, collection_name)
    if "transcript_text" in ingestion_result:
        transcript_text = ingestion_result["transcript_text"]
        video_title = ingestion_result.get("video_title", "")
        summary_result = summarize_text(transcript_text, video_title, summary_type) # Pass summary_type
        ingestion_result["summary"] = summary_result.get("summary", "Could not generate summary.")
        ingestion_result["summary_file"] = summary_result.get("summary_file", "")
        ingestion_result["language"] = language # Pass language to the result
    ingestion_result.pop("transcript_text")
    return ingestion_result

@app.post("/humanize-article")
async def humanize_article_route(original_article: str = Form(...)):
    logger.info(f"Received request to humanize article.")
    result = humanize_article_with_langgraph(original_article)
    return result

@app.post("/generate-linkedin-post")
async def generate_linkedin_post_route(article_text: str = Form(...)):
    logger.info(f"Received request to generate LinkedIn post.")
    from backend.llm_client import generate_linkedin_post
    result = generate_linkedin_post(article_text)
    return result

@app.post("/generate-posts")
async def generate_posts_route(
    youtube_url: Optional[str] = Form(None),
    text_input: Optional[str] = Form(None),
    user_prompt: str = Form(...)
):
    if not youtube_url and not text_input:
        return {"error": "Either a YouTube URL or text input must be provided."}

    from backend.ingest import get_youtube_transcript # Import the new function

    content_for_posts = ""
    if youtube_url:
        transcript_result = get_youtube_transcript(youtube_url)
        if "transcript_text" in transcript_result:
            content_for_posts = transcript_result["transcript_text"]
        else:
            return {"error": transcript_result.get("error", "Could not retrieve transcript from YouTube URL.")}
    elif text_input:
        content_for_posts = text_input

    # Generate 3 posts (this will require a new LLM function)
    # For now, let's assume a placeholder function `generate_ai_ml_posts`
    # This function will need to be created in llm_client.py
    from backend.post_generator import generate_and_humanize_posts

    result = generate_and_humanize_posts(content_for_posts, user_prompt)
    if "error" in result:
        return {"error": result["error"]}
    return {"posts": result["posts"]}

@app.get("/ask")
async def ask(query: str, collection_name: Optional[str] = "temp_docs"):
    return answer_query(query, collection_name)
