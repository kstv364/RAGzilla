from fastapi import FastAPI, UploadFile, File, Form
from backend.ingest import ingest_pdf, ingest_youtube
from backend.rag import answer_query
from backend.llm_client import summarize_text
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from dotenv import load_dotenv
import os
import logging
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
    summary_type: Optional[str] = Form("study_guide") # New parameter for summary type
):
    ingestion_result = ingest_youtube(youtube_url, collection_name)
    if "transcript_text" in ingestion_result:
        transcript_text = ingestion_result["transcript_text"]
        video_title = ingestion_result.get("video_title", "")
        summary_result = summarize_text(transcript_text, video_title, summary_type) # Pass summary_type
        ingestion_result["summary"] = summary_result.get("summary", "Could not generate summary.")
        ingestion_result["summary_file"] = summary_result.get("summary_file", "")
    ingestion_result.pop("transcript_text")
    return ingestion_result

@app.get("/ask")
async def ask(query: str, collection_name: Optional[str] = "temp_docs"):
    return answer_query(query, collection_name)
